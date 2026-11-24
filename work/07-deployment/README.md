# Deployment — `ai-agent-py`

Status: Deployment specification · 2026-11-24

This pack defines how the modular monolith is packaged, configured, delivered, migrated, and
rolled back. It is design guidance: no Dockerfiles, CI workflows, infrastructure definitions,
migration tooling, or deployment pipeline exist in the repository today.

## Current deployment state

| Area | Current |
| --- | --- |
| Runtime | Local CLI via `uv run ai-agent-py` |
| Packaging | Python package built by `uv_build`; module `ai_agent` |
| Configuration | `.env` loaded by `python-dotenv`; missing keys fail at import |
| State | SQLite file `conversations.db` created by `ConversationStore` |
| Providers | OpenAI SDK path; Ollama adapter written but dependency missing |
| Container | No `Dockerfile` or Compose file |
| CI/CD | No workflow or pipeline |
| Migrations | `CREATE TABLE IF NOT EXISTS` only; no versioning |
| Rollback | No documented procedure (this pack defines one) |
| Observability | CLI prints text and token counts only |

## Documents

| File | Purpose |
| --- | --- |
| `docker.md` | Proposed container image, Compose setup, runtime security |
| `ci-cd.md` | Pipeline stages, promotion gates, artifacts, secrets |
| `environment-configuration.md` | Variables and configuration by environment |
| `infrastructure.md` | Runtime topology, resources, network, data, operations |
| `database-migrations.md` | SQLite schema versioning, expansion/contraction, verification |
| `rollback-strategy.md` | Code, config, model, data, and provider rollback procedures |

## Deployment principles

1. Build one immutable artifact per commit; promote the same artifact through environments.
2. Keep secrets out of images, source, and CI logs; inject at runtime.
3. Configuration is explicit and validated at startup; fail closed on missing/invalid values.
4. Gate promotion on tests, lint, safety checks, and evaluation evidence.
5. Back up durable state before migrations; prefer expand-then-contract schema changes.
6. Make rollback a tested procedure, not an undocumented hope.
7. Keep the modular monolith as one process (`ADR-001`); external providers and databases remain
   outside it.
8. Never deploy with placeholder provider IDs, `context_window=0`, or unresolved critical gates.

## Traceability

Uses discovery IDs `BR-09`, `FR-15`, `NFR-05`, `NFR-06`, `NFR-08`, `NFR-11`, `NFR-12`, `NFR-13`,
implementation gates in `../04-implementation/quality-gates.md`, and ADRs in
`../02-architecture/architecture-decisions.md`.

## Reading order

1. `environment-configuration.md` for inputs to a deployment.
2. `docker.md` for packaging.
3. `ci-cd.md` for delivery and promotion.
4. `infrastructure.md` for the target runtime.
5. `database-migrations.md` for schema changes.
6. `rollback-strategy.md` for recovery.

## Status convention

- **Current** — observable in the checkout.
- **Target** — intended deployment design.
- **Proposed** — requires owner/platform approval, especially infrastructure sizing and cloud
  choices.
- **Gap** — current state blocks deployment readiness.
