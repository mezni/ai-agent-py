# Contributing

Status: Development guidelines · 2026-11-24

## Setup

```bash
uv sync
cp .env.example .env
uv run ai-agent-py
uv run pytest -q
uv run ruff check .
```

See `DEVELOPMENT.md` for configuration details. Use `.env` for local secrets; never commit it.

## Branch and change workflow

1. Create a small branch for one logical change.
2. Read the relevant requirement/ADR before changing behavior.
3. Implement with tests; use fakes and temporary SQLite databases, not live providers.
4. Run focused tests first, then the full suite and Ruff.
5. Update documentation for behavioral/decision changes (`LOG.md`, `docs/SUMMARY.md`, `work/`).
6. Open a review with evidence: commands run, results, and known limitations.
7. Do not merge with failing gates; waivers need owner, requirement ID, expiry, and mitigation.

Commit messages in this repository use conventional prefixes such as `docs:`, `test:`, `fix:`,
`refactor:`, and `feat:`. Keep commits focused and do not include secrets, credentials, API keys,
raw tickets, model outputs, or generated artifacts.

## Coding rules

| Rule | Reason |
| --- | --- |
| Application code depends on ports, not SDKs or environment variables | `ADR-001`, testability |
| Domain has no provider, web, DB, or config imports | Keeps core model stable |
| Provider-specific errors/usage normalize at the adapter boundary | Consistent behavior across providers |
| Tools require allowlist + strict Pydantic argument validation | Prevents unintended execution |
| Treat tool results, memory, summaries, and retrieved text as untrusted data | Prompt-injection boundary |
| Owner IDs must come from authenticated context, never prompt/user text | Security requirement |
| Consequential actions require a recorded human approval | `BR-03` |
| Parse only complete, validated responses | `ADR-003` |
| Secrets never enter source, logs, traces, prompts, or test fixtures as real values | `SR-10`/`SR-11` |
| Prefer explicit dependency injection from a composition root | Maintainability |

## Changes requiring an ADR

- Adding/removing a provider, model contract, or layer boundary.
- Choosing persistence, identity, approval, fallback, or observability architecture.
- Introducing a new trust boundary or external data source.
- Superseding an accepted ADR: write a new ADR and retain the old one.

Index and pending topics: `../02-architecture/architecture-decisions.md`.

## Documentation expectations

| Change | Update |
| --- | --- |
| New requirement/scope decision | `../01-discovery/` and `PRODUCT.md` |
| Architecture boundary | ADR, `ARCHITECTURE.md`, `../02-architecture/` |
| API signature/behavior | `API.md` and `DEVELOPMENT.md` |
| Test strategy/gate | `TESTING.md`, `../04-implementation/` |
| Security control/threat | `SECURITY.md`, `../06-security/` |
| Deployment/ops behavior | `DEPLOYMENT.md`, `OPERATIONS.md`, `RUNBOOK.md` |
| Learning/progress note | `LOG.md` and `docs/SUMMARY.md` |
| User-visible behavior | root `README.md` and this `README.md` |

## Review checklist

- [ ] Change is scoped to one concern and linked to requirement/issue/ADR.
- [ ] Tests added/updated; fakes used; no live API dependency.
- [ ] `uv run pytest -q` and `uv run ruff check .` results recorded.
- [ ] No secrets/PII/raw model output in diff, logs, docs, or artifacts.
- [ ] Error paths and retry limits handled explicitly.
- [ ] Owner scoping and approval path preserved where relevant.
- [ ] Metrics/logs/traces include required fields and redaction where relevant.
- [ ] Docs/ADRs/CHANGELOG updated as required.
- [ ] Backward compatibility or migration/rollback considered.

## Definition of done

A change is done when it is implemented, tested, linted, documented, reviewed, and reproducible from
a clean checkout without live credentials. “Unmeasured” or “not wired” must be stated explicitly.

## Traceability

Supports `BR-11`, `NFR-09`, `NFR-13`, M-13–M-15, and `../04-implementation/release-checklist.md`.
