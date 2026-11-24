# `ai-agent-py` Documentation Pack

Status: Engineering handoff pack · 2026-11-24

Goal: make the project understandable, maintainable, and usable by another engineering team without
 relying on the original author's memory.

These documents complement, but do not replace, the repository's root `README.md`,
`docs/SUMMARY.md`, and `LOG.md`. They consolidate the work specs into a single onboarding path and
state clearly which behavior is implemented, partial, or only proposed.

## Current project snapshot

| Item | Current |
| --- | --- |
| Version | `0.1.0` in `pyproject.toml` |
| Runtime | Python 3.12+, `uv`, console script `ai-agent-py` |
| Entrypoint | `src/ai_agent/main.py` runs one hardcoded ticket through `CustomerSupportAssistant` |
| Tests | 57 pass when two broken modules are excluded; full collection fails |
| Lint | `uv run ruff check .` reports 8 pre-existing errors |
| CI/CD | None |
| API service | None; CLI and importable Python modules only |
| Persistence | SQLite file `conversations.db`; no migration tool |
| Evaluation | No dataset/harness or results; targets in `../01-discovery/success-metrics.md` are proposed |
| Documentation state | `../03-design/` is partial; `../05-evaluation/` has not been created |

## Documents

| Document | Purpose |
| --- | --- |
| `README.md` | This index: project overview, setup pointers, and documentation map |
| `PRODUCT.md` | Business objectives, product scope, users, and success criteria |
| `ARCHITECTURE.md` | System shape, layers, flows, decisions, and current violations |
| `CONTRIBUTING.md` | Development workflow, coding rules, reviews, and definition of done |
| `API.md` | Imported Python API; there is no HTTP API today |
| `DEVELOPMENT.md` | Local development instructions and common commands |
| `TESTING.md` | Testing strategy, inventory, baseline, and required additions |
| `SECURITY.md` | Trust boundaries, controls, gaps, and safe usage rules |
| `DEPLOYMENT.md` | Packaging, configuration, infrastructure, migrations, rollback |
| `OPERATIONS.md` | Observability, health, monitoring, alerts, cost, troubleshooting |
| `RUNBOOK.md` | Step-by-step operational procedures |
| `CHANGELOG.md` | Version history and release evidence expectations |
| `LOG.md` | Learning and implementation progress summary |

## Quick start pointers

- Root quick start: `../../README.md`
- Lesson summaries: `../../docs/SUMMARY.md`
- Development log: `../../LOG.md`
- Local setup: `DEVELOPMENT.md`
- Verification: `TESTING.md`
- Architecture detail: `../02-architecture/README.md`
- Requirements: `../01-discovery/README.md`
- Implementation plan: `../04-implementation/README.md`
- Security: `../06-security/README.md`
- Deployment: `../07-deployment/README.md`
- Operations: `../08-operations/README.md`

## Source-of-truth rules

1. Code is the source of truth for implemented behavior.
2. ADRs in `../02-architecture/adr/` are the source of truth for accepted design decisions.
3. `../01-discovery/` is the source of truth for requirements and proposed targets.
4. Evaluation results, when created, must include method/version metadata; unmeasured means
   unmeasured, not zero or passing.
5. This pack is the handoff summary; if it conflicts with code, update the pack and record the
   discrepancy.
6. Never promote an unimplemented target to “current” in documentation.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| Current | Observable in the checkout |
| Partial | Code exists but is incomplete, unwired, or broken |
| Target | Intended design; not yet implemented |
| Proposed | Requires owner approval |
| Gap | Blocks release/readiness |

## Known handoff gaps

- Resolve the two conflicting `ModelClient` contracts (`Q-12`, pending ADR-004).
- Fix `OpenAIProvider.stream()` (`Iterator`, `self.model`, event iteration/yields).
- Fix undefined `LLMValidationError` in `ticket_validation.py`.
- Resolve `config.py` shadowing `config/`.
- Declare or guard the `ollama` dependency.
- Add evaluation dataset/harness and measured M-01–M-12 results.
- Add authentication, owner scoping, approval gate, redaction, CI/CD, and migration tooling.

## Traceability

Supports `BR-11` and the documentation/decision coverage metric M-15 in
`../01-discovery/success-metrics.md`.
