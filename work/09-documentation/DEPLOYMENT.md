# Deployment

Status: Current state and target instructions · 2026-11-24

## Current state

There is no Dockerfile, CI workflow, infrastructure definition, migration tool, or deployment
pipeline. Deployment today means a developer checkout:

```bash
uv sync
cp .env.example .env
uv run ai-agent-py
```

The CLI is not a long-running service. State is a local SQLite file created on first
`ConversationStore` construction.

## Prerequisites before real deployment

- Full tests and lint pass (`TESTING.md`).
- Canonical model contract recorded (`ADR-004`) and applied.
- `config.py`/`config/` shadowing resolved.
- Provider/model IDs and capabilities verified.
- Authentication, owner scoping, approval gate, and redaction implemented and tested.
- Evaluation gates G3–G5 accepted with evidence.
- Backup/migration/rollback procedures rehearsed.

## Configuration

| Variable | Current | Target |
| --- | --- | --- |
| `OPENAI_API_KEY` | Required by `config.py` | Secret store/injected env |
| `OPENAI_MODEL` | Required by `config.py` | Approved model ID |
| `LLM_PROVIDER` | Not implemented | `openai` or `ollama` |
| `OLLAMA_MODEL` / `OLLAMA_BASE_URL` | Not implemented | Local provider only |
| `DB_PATH` | Not implemented | Mounted/approved path |
| `LOG_LEVEL`, limits, profile, prices, flags | Not implemented | Validated at startup |

Missing/invalid configuration must fail the deployment with a clear error, never echo values, and
never default to a placeholder provider/model. Full matrix:
`../07-deployment/environment-configuration.md`.

## Packaging

Target is one immutable container per commit SHA, built with locked dependencies and a non-root
user. Secrets are injected at runtime; images never contain `.env`, keys, raw data, or source
artifacts. See `../07-deployment/docker.md` for the proposed Dockerfile/Compose topology.

## CI/CD promotion

| Stage | Gate |
| --- | --- |
| Install | `uv sync --frozen` |
| Lint | `uv run ruff check .` → 0 errors |
| Test | `uv run pytest -q` → 0 failures/collection errors |
| Config smoke | Settings/profiles/catalog import |
| Security | Secret scan, dependency scan, redaction tests |
| Build | Image built and scanned |
| Evaluation | M-01–M-10 reported; G3/G4 passed |
| Staging | G2–G4; migration and rollback rehearsed |
| Production | G5 + owner sign-off |

Promote the same artifact through environments. Do not use `:latest` for production. Full pipeline:
`../07-deployment/ci-cd.md`.

## Infrastructure

Target: one application process/container, approved LLM provider, optional restricted Ollama
service, private durable state, secret store, and redacted observability sink. Sizing is proposed
and unmeasured; horizontal scaling against a single SQLite file is not supported until ADR-008.
See `../07-deployment/infrastructure.md`.

## Database migrations

Current schema is created with `CREATE TABLE IF NOT EXISTS`; there is no version table or down
path. Target migrations are explicit, versioned, checksummed, and applied before app start. Back up
before every migration; prefer expand-then-contract for owner columns. Details and verification
queries: `../07-deployment/database-migrations.md`.

## Rollback

Every release record must name a previous known-good artifact, config, provider/model/prompt/profile,
and schema version. Roll back code/config first; use down migration or verified backup for schema
changes; preserve evidence. See `../07-deployment/rollback-strategy.md` and `RUNBOOK.md`.

## Deployment checklist

- [ ] Gates G2–G5 passed or explicitly waived.
- [ ] Same artifact promoted; SHA/digest recorded.
- [ ] Secrets injected and scanned; no values logged.
- [ ] Provider/model/profile/prompt/context/retry explicit.
- [ ] DB path writable; backup verified; migration version expected.
- [ ] Auth/owner/approval controls enabled.
- [ ] Health/readiness checks available when a transport exists.
- [ ] Rollback target recorded and rehearsed.
- [ ] Release record links test/lint/evaluation/security evidence.

## Traceability

Supports `BR-09`, `FR-15`, `NFR-08`, `NFR-11`, `NFR-12`, and `../07-deployment/README.md`.
