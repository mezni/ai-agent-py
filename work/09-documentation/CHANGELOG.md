# Changelog

Status: Version history template and current summary · 2026-11-24

## Format

Use a reverse-chronological, Keep-a-Changelog-style structure with `Added`, `Changed`, `Fixed`,
`Removed`, `Security`, and `Known issues`. Every release entry links evidence: code revision,
test/lint results, evaluation/security reports, provider/model/profile/prompt versions, migration
version, and rollback target. Mark unmeasured items explicitly.

## [Unreleased]

### Added

- `work/01-discovery/`: discovery brief, stakeholder-interview template, business/functional/
  non-functional requirements, assumptions, and proposed success metrics.
- `work/02-architecture/`: system context, container/component/data-flow views, decision index, and
  ADR-001–ADR-003.
- `work/03-design/`: README and domain model (remaining design documents pending).
- `work/04-implementation/`: setup, implementation/component/refactor plans, testing strategy,
  quality gates, and release checklist.
- `work/06-security/`: threat model, SR-01–SR-22, prompt-injection, PII, access-control, and
  secrets-management specs.
- `work/07-deployment/`: Docker, CI/CD, environment, infrastructure, migration, and rollback specs.
- `work/08-operations/`: logging, metrics, tracing, monitoring, alerting, cost, and incident specs.
- `work/09-documentation/`: this engineering handoff pack.

### Changed

- None in runtime behavior as part of the documentation packs.

### Fixed

- None; known implementation blockers remain listed below.

### Security

- No security controls changed in code; required controls are specified in `SECURITY.md` and
  `../06-security/`.

### Known issues

- Full pytest collection fails on `Iterator` and `LLMValidationError`.
- `uv run ruff check .` reports 8 errors.
- Conflicting `ModelClient` contracts; pending `ADR-004`.
- `config.py` shadows `config/`.
- `ollama` dependency missing; streaming incomplete.
- No auth, owner scoping, approval gate, evaluation harness, CI/CD, migrations, or observability
  implementation.

## [0.1.0]

Current package version in `pyproject.toml`. This represents the staged learning/reference project,
not a production release. No formal release evidence record was provided in the checkout.

### Included components

- CLI entry point and `CustomerSupportAssistant` answer path via OpenAI Responses API.
- `OpenAIProvider` with basic usage mapping and error translation; `OllamaProvider` written but not
  importable.
- Prompt templates/registry/builder and ticket classification schema/parser/validator.
- Tool registry, strict argument schemas, dispatcher/executor, and mock order/customer/FAQ data.
- Conversation store/manager/context manager with SQLite persistence and token budgeting.
- Memory summarizer/extractor/retriever/manager and owner-scoped long-term memory table.
- Retry/error taxonomy, generation options/profiles, model registry/selector/catalog.
- Streaming helpers and unit tests using fakes/temporary databases.

### Known limitations at 0.1.0

- CLI message is hardcoded; tool/memory/orchestration modules are not fully wired.
- Provider contract conflict and broken streaming/validation imports.
- Profiles/catalog unimportable due to config shadowing.
- No live-provider contract suite, evaluation results, CI, deployment, or operations implementation.

## Release evidence template

| Field | Value |
| --- | --- |
| Version / revision |  |
| Date |  |
| Provider / model / profile / prompt version |  |
| Context limits / retry policy |  |
| Dataset version / evaluation report |  |
| Test result / lint result |  |
| Security result / waivers |  |
| Migration version / backup result |  |
| Rollback target |  |
| Approvals |  |

## Traceability

Supports `BR-11`, M-15, `../04-implementation/release-checklist.md`, and
`../07-deployment/ci-cd.md`.
