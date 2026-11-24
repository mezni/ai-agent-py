# Architecture — `ai-agent-py`

Status: Draft · 2026-11-24

This pack translates the discovery requirements in `../01-discovery/` into views of the system:
its external context, deployable containers, internal components, and data flows. It describes
both the **current** implementation and the **target** design; every discrepancy is called out
rather than hidden.

## Relationship to discovery

Architecture decisions must trace to stable discovery IDs:

- `BR-xx` — business outcome
- `FR-xx` — observable behavior
- `NFR-xx` — quality constraint
- `Q-xx` — unresolved question

For example, the canonical model-client decision addresses `FR-02`, `FR-07`, `FR-10`,
`NFR-09`, and open question `Q-12`.

## Documents

| File | View |
| --- | --- |
| `system-context.md` | System boundary, actors, external systems, trust boundaries |
| `container-diagram.md` | Deployable/runtime containers and communication paths |
| `component-diagram.md` | Internal modules, layers, dependency rules, current violations |
| `data-flow.md` | Request, tool, memory, streaming, and failure data flows |
| `architecture-decisions.md` | Decision index, lifecycle, pending decisions |
| `adr/ADR-001-modular-monolith.md` | Why one layered deployable instead of distributed services |
| `adr/ADR-002-llm-classification.md` | Why classification is LLM-based and validated |
| `adr/ADR-003-structured-output.md` | How machine-readable output is produced and trusted |

## Reading order

1. `../01-discovery/discovery-brief.md` for problem and scope.
2. `system-context.md` for what is inside and outside the system.
3. `container-diagram.md` for runtime boundaries.
4. `component-diagram.md` for code organization and dependency rules.
5. `data-flow.md` for how information moves and where trust changes.
6. `architecture-decisions.md` and the ADRs for the reasoning behind the design.

## Evidence base

| Source | Use |
| --- | --- |
| `src/ai_agent/**` | Observed components and dependencies |
| `README.md`, `LOG.md` | Design intent and documented gaps |
| `tests/**` | What is actually verifiable today |
| `pyproject.toml`, `.env.example` | Runtime/deployment constraints |
| `../01-discovery/**` | Requirements, assumptions, constraints, metrics |

## Status convention

- **Current** — observable in the checkout.
- **Target** — intended design; may be partially implemented.
- **Gap** — target design not yet satisfied.
- ADR status follows `Proposed → Accepted → Superseded | Deprecated`.

## Architectural principles

1. **Dependency inversion:** application code depends on ports such as `ModelClient`, not on SDKs.
2. **Thin adapters:** provider, storage, and tool integrations translate at the boundary.
3. **One authority for business state:** tools, databases, and application code are authoritative;
   model output, history, and memory are supporting context only.
4. **Validate at trust boundaries:** user text, provider output, tool results, and stored memory are
   untrusted inputs.
5. **Explicit control limits:** turn budgets, tool-call budgets, retries, context budgets, and
   human approval are enforced in application code.
6. **Reproducibility:** prompts, models, generation profiles, tool schemas, and datasets are
   versioned so evaluations and incidents can be replayed.

## Known architectural debt

| Gap | Impact | Related IDs |
| --- | --- | --- |
| `ModelClient` string protocol coexists with `ModelRequest`/`ModelResponse` | Provider substitution and tests are inconsistent | `FR-02`, `FR-07`, `FR-10`, `Q-12` |
| `AgentOrchestrator` constructs `OpenAI` and reads `OPENAI_MODEL` directly | Violates dependency inversion; hard to test | `FR-04`, `NFR-09` |
| `ticket_classifier.py` constructs `OpenAI` and reads the environment directly | Classification is not provider-agnostic | `FR-02`, `ADR-002` |
| `config.py` shadows `config/` so profiles/catalog cannot be imported | Configuration layer is broken | `NFR-09`, `NFR-11` |
| `OpenAIProvider.stream()` has undefined `Iterator` and `self.model` | Full test collection and lint fail | `FR-07`, `NFR-12` |
| `ticket_validation.py` imports undefined `LLMValidationError` | Structured-validation path fails at import | `FR-02`, `ADR-003` |
| `OllamaProvider` depends on an undeclared `ollama` package | Local provider cannot be imported | `FR-10`, `NFR-11` |
| No provider factory, auth layer, approval gate, or production DB | Target boundaries are not yet enforced | `FR-05`, `FR-06`, `FR-09`, `FR-10` |

## Pending decisions to record

| Topic | Question | Target ADR |
| --- | --- | --- |
| Canonical model contract | String protocol or request/response model? | ADR-004 (`Q-12`) |
| Provider factory and fallback | Configuration, capability checks, failure policy | ADR-005 |
| Identity and owner scoping | How authenticated `owner_id` reaches storage and tools | ADR-006 |
| Approval workflow | Which actions require approval and how decisions are recorded | ADR-007 |
| Persistence and migrations | SQLite file vs. managed database, schema evolution | ADR-008 |
| Observability stack | Metrics, logs, traces, redaction, retention | ADR-009 |

## Change process

When an architectural choice changes, update the affected view, the requirement trace, and the
ADR. Do not delete superseded ADRs; add a new ADR that references the old one. Diagrams describe
the current agreed design, while ADRs preserve why alternatives were rejected.
