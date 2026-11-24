# Implementation — `ai-agent-py`

Status: Implementation planning · 2026-11-24

This pack describes how to build, refactor, verify, and release the system defined in
`../01-discovery/`, `../02-architecture/`, and the available `../03-design/` documents. It focuses
on executable work: order of changes, configuration, component-level guidance, tests, gates, and
release readiness.

## Relationship to other phases

| Phase | Question answered |
| --- | --- |
| `../01-discovery/` | Why build it, for whom, and what success means |
| `../02-architecture/` | Boundaries, layers, decisions, trust zones |
| `../03-design/` | Domain objects, classes, contracts, data, rules, errors |
| `../04-implementation/` | What to change, in what order, and how to verify it |
| `../05-evaluation/` | How to measure quality and guard against regressions |

At the time of writing, `03-design` contains only `README.md` and `domain-model.md`; the remaining
design documents have not been created. This pack does not assume their contents.

## Documents

| File | Purpose |
| --- | --- |
| `implementation-plan.md` | Phased build sequence, dependencies, deliverables, exit criteria |
| `setup-and-configuration.md` | Environment, dependencies, settings, commands, troubleshooting |
| `component-implementation.md` | Component-by-component current state, target changes, tests |
| `refactor-plan.md` | Ordered code migrations for known architectural debt |
| `testing-strategy.md` | Test layers, fakes, coverage, failure injection, CI |
| `quality-gates.md` | Gate definitions, thresholds, current status, waivers |
| `release-checklist.md` | Pre-release verification and sign-off checklist |

## Current implementation snapshot

| Area | Current state |
| --- | --- |
| CLI | One-shot `main.py` with a hardcoded ticket and printed token counts |
| Model path | `CustomerSupportAssistant` uses `ModelRequest`/`ModelResponse` via `OpenAIProvider.generate()` |
| Streaming | `Assistant.ask_stream()` exists; `OpenAIProvider.stream()` is incomplete and breaks collection |
| Classification | Prompt/parser/retry modules exist; classifier constructs `OpenAI` directly; validator import fails |
| Tools | Allowlisted registry, strict schemas, dispatcher, mock order/customer/FAQ handlers |
| Orchestration | 5-turn / 10-tool-call loop exists; constructs `OpenAI`, reads env, embeds prompts |
| Conversation | SQLite store, context manager, conversation manager; not wired to the CLI/orchestrator |
| Memory | Summarizer/extractor/retriever/manager and owner-scoped table; not wired to context/orchestrator |
| Generation/model config | Frozen config, registry, selector, profiles, catalog; config package cannot be imported |
| Providers | OpenAI adapter partial; Ollama adapter written but dependency undeclared |
| Quality gates | Full pytest collection fails; Ruff reports 8 pre-existing errors; no CI or typechecker |
| Security | `.env` ignored; no auth, owner-derived identity, approval gate, audit, or redaction |

## Status convention

- **Current** — observable in the checkout.
- **Target** — intended implementation.
- **Gap** — current code contradicts the target.
- **Proposed** — depends on an unresolved decision such as `Q-12` or pending `ADR-004`.

## Command quick reference

| Command | Purpose |
| --- | --- |
| `uv sync` | Install runtime and dev dependencies from the lockfile |
| `cp .env.example .env` | Create local configuration; never commit the result |
| `uv run ai-agent-py` | Run the current one-shot CLI |
| `uv run pytest -q` | Run the full test suite once collection is fixed |
| `uv run ruff check .` | Lint the repository |
| `uv run ruff check <path>` | Lint changed paths |

## Traceability

Implementation work references discovery IDs (`BR-xx`, `FR-xx`, `NFR-xx`), architecture decisions
(`ADR-001`–`ADR-003`), and open questions (`Q-xx`). A change that alters an architectural boundary
requires a new or updated ADR before it is implemented.

## Reading order

1. `implementation-plan.md` for sequence and priorities.
2. `setup-and-configuration.md` for the working environment.
3. `refactor-plan.md` for existing-code migrations.
4. `component-implementation.md` for component-specific detail.
5. `testing-strategy.md` and `quality-gates.md` for verification.
6. `release-checklist.md` for final readiness.

## Change process

Every implementation change must update the affected test, the affected spec document, and the
quality-gate evidence. Do not mark a target behavior complete when only a module exists; completion
requires the end-to-end path and its tests to work.
