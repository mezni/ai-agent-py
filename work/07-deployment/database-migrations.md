# Database Migrations

Status: Current schema and target migration policy · 2026-11-24

## Current schema

`src/ai_agent/application/conversation_store.py` creates four tables at construction time with
`CREATE TABLE IF NOT EXISTS`. There is no migration tool, version table, checksum, or down script.

| Table | Columns | Indexes / constraints | Notes |
| --- | --- | --- | --- |
| `conversations` | `id TEXT PK`, `created_at TEXT NOT NULL` | — | No owner; any ID is addressable |
| `messages` | `id TEXT PK`, `conversation_id TEXT NOT NULL`, `role TEXT NOT NULL`, `content TEXT NOT NULL`, `created_at TEXT NOT NULL` | FK `conversation_id → conversations.id ON DELETE CASCADE`; index `idx_messages_conversation` | No owner; messages inherit unowned conversation |
| `conversation_memory` | `conversation_id TEXT PK`, `summary TEXT NOT NULL`, `facts TEXT NOT NULL` | FK `conversation_id → conversations.id ON DELETE CASCADE` | JSON `facts` |
| `long_term_memories` | `id TEXT PK`, `owner_id TEXT NOT NULL`, `memory_key TEXT NOT NULL`, `memory_value TEXT NOT NULL`, `confidence REAL NOT NULL`, `source TEXT NOT NULL`, `created_at TEXT NOT NULL`, `updated_at TEXT NOT NULL` | `UNIQUE(owner_id, memory_key)`; index `idx_memory_owner` | Owner is caller-supplied today |

Connections set `PRAGMA foreign_keys = ON` and use parameterized SQL. The schema is created on
every `ConversationStore` start; in a deployed process that means first start mutates the database.

## Gaps

- No schema version or applied-migration record.
- No backup before schema change.
- No reproducible upgrade/downgrade path between revisions.
- No owner column on `conversations`/`messages`; no owner predicates in their queries.
- No transaction strategy for multi-step migrations.
- No migration tests against a copy of production-like data.
- No approval/audit record tying a migration to a release.

## Target migration framework

Add versioned SQL migrations under a dedicated directory, for example:

```text
migrations/
  001_initial_schema.up.sql
  001_initial_schema.down.sql
  002_add_conversation_owner.up.sql
  002_add_conversation_owner.down.sql
  003_add_message_owner.up.sql
  003_add_message_owner.down.sql
```

Use a small in-repo runner or an approved tool such as Alembic; no migration dependency exists
today. The runner must:

- create `schema_migrations(version INTEGER PRIMARY KEY, name TEXT, applied_at TEXT, checksum TEXT)`;
- apply only migrations greater than the recorded version;
- verify checksums before applying;
- run each migration in a transaction where SQLite permits it;
- refuse to start the application if the database version is ahead or unknown;
- log version/name/timestamp without sensitive data;
- expose `up`, `status`, and `down` commands for local/staging use;
- be invoked explicitly during deployment, not implicitly from a domain/application constructor.

## Expansion and contraction policy

Prefer additive changes that allow old and new code to run during a rolling release.

| Phase | Schema change | Code behavior | Release |
| --- | --- | --- | --- |
| 1 Expand | Add nullable `owner_id` columns/indexes | Write both old and new shape where needed; read old shape | Deploy N |
| 2 Backfill | Populate from trusted identity data | Continue reading both | Job/verification |
| 3 Enforce | Add predicates; require owner from `Principal` | Read/write new shape only | Deploy N+1 |
| 4 Contract | Rebuild tables to `NOT NULL`, remove legacy columns if any | New shape only | Deploy N+2 after verification |

SQLite cannot safely add a `NOT NULL` column with a non-constant default to a populated table via
`ALTER TABLE` alone. Table rebuild requires:

1. disable foreign keys outside a transaction;
2. create a new table with the final schema;
3. copy validated rows;
4. drop/rename old table;
5. recreate indexes and triggers;
6. re-enable foreign keys and run integrity checks.

This sequence needs rehearsal and a tested backup; down migrations are not guaranteed for
irreversible data transformations.

## Migration sequence example

| Version | Change | Up risk | Down | Verification |
| --- | --- | --- | --- | --- |
| 001 | Record current four-table schema | Low | Drop tables only in disposable environments | Row counts and indexes match current |
| 002 | Add nullable `conversations.owner_id` + index | Low | Drop column/index | All conversations assigned or explicitly pending |
| 003 | Add nullable `messages.owner_id` + index; backfill from conversation | Medium | Drop column/index | No message has null/owner mismatch |
| 004 | Owner predicates in store methods | App change | Revert app | Cross-owner tests pass |
| 005 | Rebuild tables with `NOT NULL` owners if required | High | Restored backup only | `PRAGMA foreign_key_check`, integrity check, smoke tests |

Exact migrations depend on ADR-006/ADR-007 and the chosen identity source. Do not backfill from
untrusted prompt/tool data.

## Procedure

1. Record release version, code revision, current schema version, and rollback target.
2. Take and verify a backup of the database file/volume.
3. Run `migrations status` and confirm the expected applied version/checksum.
4. Apply migrations on a restored copy and run verification queries.
5. Apply to target environment; stop batch/CLI work that writes state.
6. Run integrity checks and smoke tests.
7. Deploy/enable application code that matches the new version.
8. Record applied version and evidence in the release record.

## Verification queries

```sql
SELECT version, name, applied_at FROM schema_migrations ORDER BY version;
PRAGMA integrity_check;
PRAGMA foreign_key_check;
SELECT COUNT(*) FROM conversations WHERE owner_id IS NULL;
SELECT COUNT(*) FROM messages WHERE owner_id IS NULL;
SELECT COUNT(*) FROM messages m
LEFT JOIN conversations c ON c.id = m.conversation_id
WHERE c.id IS NULL OR c.owner_id <> m.owner_id;
SELECT name FROM sqlite_master WHERE type = 'index' ORDER BY name;
```

Expected results before enforcement: zero rows for orphan/mismatch queries and zero null owners once
backfill is complete.

## Tests

- Fresh database applies all migrations and matches the expected schema snapshot.
- Every migration has an `up` test and a `down` test where safe.
- Existing four-table database upgrades cleanly.
- Ahead/unknown schema version blocks startup.
- Checksum mismatch blocks startup.
- Failed migration leaves recoverable state and is recorded.
- Owner backfill uses only trusted identity data.
- Production-like copy passes verification queries and smoke tests.

## Traceability

Supports `BR-08`, `FR-03`, `FR-15`, `NFR-06`, `NFR-08`, `SR-03`, and
`../06-security/access-control.md`.
