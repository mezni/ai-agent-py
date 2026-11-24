# Design — `ai-agent-py`

Status: Detailed design · 2026-11-24

This pack refines the architecture in `../02-architecture/` into implementable design: domain
objects, class structure, contracts, interaction flows, persistence, business rules, and errors.

## Relationship to earlier phases

| Phase | Question answered |
| --- | --- |
| `../01-discovery/` | Why are we building this, for whom, and what counts as success? |
| `../02-architecture/` | What are the boundaries, layers, external systems, and decisions? |
| `../03-design/` | What are the exact objects, contracts, rules, data, and failure semantics? |

Requirements use the stable IDs from discovery (`BR-xx`, `FR-xx`, `NFR-xx`) and decisions use the
ADRs from architecture (`ADR-001`–`ADR-003`). Open questions remain `Q-xx`.

## Documents

| File | Content |
| --- | --- |
| `domain-model.md` | Domain language, objects, aggregates, invariants, lifecycle, authority |
| `class-diagram.md` | Classes, attributes, methods, relationships, dependency gaps |
| `api-contracts.md` | Internal Python contracts, CLI surface, proposed transport surface |
| `sequence-diagrams.md` | Method-level flows for classification, tools, conversation, streaming, failures |
| `database-schema.md` | SQLite tables, columns, constraints, indexes, upserts, migration gaps |
| `business-rules.md` | Classification, tool, memory, context, approval, and generation rules |
| `error-catalog.md` | Error taxonomy, triggers, handling, retryability, user impact |

## Status convention

- **Current** — matches the checkout exactly, including defects.
- **Target** — design intent; not yet implemented.
- **Gap** — current behavior contradicts the target and needs a change.
- **Proposed** — subject to an unresolved decision such as `Q-12` or `ADR-004`.

## Evidence base

All current signatures, fields, table definitions, and rules are taken from:

- `src/ai_agent/domain/**`
- `src/ai_agent/application/**`
- `src/ai_agent/prompts/**`
- `src/ai_agent/providers/**`
- `src/ai_agent/tools/**`
- `src/ai_agent/config.py`, `src/ai_agent/config/**`
- `tests/**`
- `pyproject.toml`, `README.md`

`docs/SUMMARY.md` is lesson-oriented and may contain stale status claims; code is the stronger
source for current design facts.

## Design principles

1. Domain objects carry data and invariants; application services coordinate work.
2. Ports and adapters isolate providers, storage, and tools (`ADR-001`).
3. Only complete, validated model output is trusted (`ADR-003`).
4. Tool results, memory, summaries, and user text are untrusted data.
5. Business authority stays in tools, databases, and application code.
6. Every failure has a class, an owner, a retry decision, and a user-appropriate outcome.
7. Contracts must be testable with fakes and without live API keys.

## Known design blockers

| Blocker | Consequence | Related docs |
| --- | --- | --- |
| Two incompatible model interfaces | Provider substitution and structured output cannot share one port | `api-contracts.md`, `ADR-004` |
| `LLMValidationError` is imported but not defined | Full test collection fails | `business-rules.md`, `error-catalog.md` |
| `OpenAIProvider.stream()` has undefined `Iterator` and `self.model` | Streaming contract is unusable | `api-contracts.md`, `sequence-diagrams.md` |
| `config.py` shadows `config/` | Generation profiles and model catalog cannot be imported | `class-diagram.md`, `business-rules.md` |
| `owner_id` is not part of `Conversation` | Owner scoping is incomplete at the domain level | `domain-model.md`, `database-schema.md` |
| Model catalog uses placeholder IDs and `context_window=0` | Capability/context decisions cannot rely on catalog | `business-rules.md` |
| No auth, approval, or audit object exists | Authorization rules cannot be enforced in the domain today | `business-rules.md`, `api-contracts.md` |

## Reading order

1. `domain-model.md` for the vocabulary and invariants.
2. `class-diagram.md` for the structural design.
3. `api-contracts.md` for callable boundaries.
4. `sequence-diagrams.md` for runtime collaboration.
5. `database-schema.md` for durable state.
6. `business-rules.md` and `error-catalog.md` for policy and failure behavior.

## Change process

When a design detail changes, update the affected document, its trace IDs, and any sequence/class
diagram that shows it. If the change alters a boundary or a rejected alternative, open a new ADR
rather than rewriting architecture history. Design changes must add or update tests that exercise
the changed contract.
