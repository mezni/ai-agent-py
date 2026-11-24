# Architecture Decisions

Status: Decision index · 2026-11-24

This page indexes the architectural choices for `ai-agent-py`. Each ADR records the context,
decision, rejected alternatives, consequences, and implementation obligations. Accepted ADRs
describe the agreed direction; they do not imply the code already satisfies them.

## Decision index

| ADR | Title | Status | Date | Primary drivers |
| --- | --- | --- | --- | --- |
| `ADR-001` | Modular monolith | Accepted | 2026-11-24 | `BR-10`, `BR-11`, `FR-04`, `FR-10`, `NFR-09`, `NFR-11` |
| `ADR-002` | LLM-based ticket classification | Accepted | 2026-11-24 | `BR-02`, `FR-02`, `FR-08`, `NFR-01`, `NFR-04` |
| `ADR-003` | Validated structured output | Accepted | 2026-11-24 | `FR-02`, `FR-07`, `FR-12`, `NFR-01`, `NFR-14` |

## Requirement map

| Requirement | Supporting decision |
| --- | --- |
| `BR-04` grounded, auditable answers | ADR-001 (single process traceability), ADR-003 (validated output) |
| `BR-10` vendor independence | ADR-001 (ports and adapters), ADR-002 (provider-neutral classification) |
| `FR-03` allowlisted tools | ADR-001 (application-enforced boundaries) |
| `FR-04` bounded orchestration | ADR-001 |
| `FR-05` / `FR-06` conversation and memory | ADR-001 (injected repository/services) |
| `FR-07` streaming | ADR-003 (only complete responses are trusted) |
| `FR-08` generation settings | ADR-002 |
| `FR-13` evaluation | ADR-002, ADR-003 |
| `NFR-05` / `NFR-06` security and authorization | ADR-001 (application control boundary) |
| `NFR-09` maintainability | ADR-001, ADR-003 |

## Decision lifecycle

```text
Proposed → Accepted → Superseded by ADR-xxx | Deprecated
```

- A proposed ADR is under review and must not be treated as policy.
- An accepted ADR is the current design direction.
- A superseded or deprecated ADR is retained for history and points to its replacement.
- Never delete an old ADR; write a new one with the new context and alternatives.

Each ADR contains: **Status**, **Date**, **Context**, **Decision**, **Alternatives Considered**,
and **Consequences**. Consequences include both positive/negative effects and concrete
implementation obligations.

## Current implementation status

| ADR | Direction | Code status |
| --- | --- | --- |
| ADR-001 | One layered deployable with injected dependencies | Single process exists; SDK/env coupling and config packaging violate the target |
| ADR-002 | LLM classification through the model port with validation | Classifier exists but constructs OpenAI and reads `OPENAI_MODEL` directly |
| ADR-003 | Complete, schema- and business-validated output | Strict schema and parser exist; validation import and streaming are broken |

The gaps are tracked in `component-diagram.md` and must be closed before the ADRs can be treated
as fully realized.

## Pending decisions

| Topic | Question | Proposed ADR | Inputs needed |
| --- | --- | --- | --- |
| Canonical model contract | String `ModelClient` or `ModelRequest`/`ModelResponse`? | ADR-004 | `Q-12`, architecture review, migration estimate |
| Provider factory and fallback | How are providers selected, capability-checked, and failed over? | ADR-005 | Provider approval, limits, error taxonomy |
| Identity and owner scoping | How does authenticated `owner_id` reach tools and storage? | ADR-006 | `Q-09`, security design |
| Approval workflow | Which actions require approval and what is recorded? | ADR-007 | `Q-11`, approver interview |
| Persistence and migrations | SQLite file vs. managed database; schema evolution | ADR-008 | Volume, retention, ops model |
| Observability | Metrics, logs, traces, redaction, and retention | ADR-009 | `Q-10`, ops/SRE requirements |

## Review triggers

Reopen or supersede a decision when:

- measured quality, latency, or cost misses the targets in `../01-discovery/success-metrics.md`;
- a provider adds, removes, or changes a capability such as structured output or streaming;
- expected volume or concurrency invalidates one-process or single-file storage assumptions;
- an authorization, retention, or residency requirement changes the deployment boundary;
- a new transport, tenant, or independent deployment need appears;
- an evaluation shows a simpler alternative outperforms the chosen design.

## Verification obligations

An accepted ADR is not complete until:

1. affected diagrams and specs are updated;
2. code dependency rules match the decision;
3. tests cover the decision's critical behavior and failure paths;
4. evaluation or review evidence is recorded;
5. known deviations are listed with an owner and target date.
