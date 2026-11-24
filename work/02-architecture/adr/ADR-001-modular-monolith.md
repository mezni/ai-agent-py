# ADR-001: Modular Monolith

## Status

Accepted · 2026-11-24

This records the target design for the current phase. The checkout is a single Python process, but
several components still violate the required internal boundaries.

## Date

2026-11-24

## Context

`ai-agent-py` is a staged Python customer-support project with one CLI entry point, a SQLite file,
provider SDKs, and unit tests. There is no HTTP service, queue, worker pool, managed database,
deployment pipeline, or operations team infrastructure. The project must remain easy to run,
test, and learn from while still supporting provider substitution, tool orchestration,
conversation state, memory, evaluation, and future security controls.

Relevant constraints:

- Python 3.12+, `uv`, `pyproject.toml`, and `uv.lock` are the toolchain.
- Model quality and latency targets are not yet measured.
- `BR-10` requires vendor independence; `NFR-09` requires clean layering; `BR-11` values the
  staged engineering-reference nature of the project.
- Current debt includes direct provider construction in application code, direct environment
  reads, a broken configuration package, and two incompatible model contracts.

## Decision

Build `ai-agent-py` as a **modular monolith**: one deployable Python application with strict
internal modules and explicit dependency inversion.

1. One composition root (`src/ai_agent/main.py`) creates and injects collaborators.
2. Internal layers are entry, application, domain, prompts, providers, tools, configuration, and
   persistence.
3. Application services depend on ports such as `ModelClient`, an injected prompt builder, an
   injected tool dispatcher, and a conversation-store interface.
4. The domain layer contains only business/data models and has no provider, SDK, database, or
   web-framework imports.
5. Provider adapters own SDK/HTTP details, event streaming, generation-option mapping, and error
   normalization.
6. Tool handlers live in-process behind a registry and dispatcher; application code enforces
   allowlists, strict argument validation, authorization, and approval.
7. Conversation and memory state stay in SQLite behind a repository interface during this phase.
8. A thin CLI or transport adapter may be added, but it does not create a separate service per
   capability.

## Alternatives Considered

### Microservices per capability

Separate services for classification, orchestration, tools, memory, and providers.

- **Pros:** independent scaling/deployment, stronger isolation, polyglot options.
- **Cons:** network failure modes, distributed tracing/debugging, data consistency challenges,
  latency and infrastructure overhead, no ops foundation in the project.
- **Rejected:** costs exceed current volume and learning goals; premature distribution would
  obscure the LLM-specific risks the project is meant to study.

### Serverless functions per request step

- **Pros:** elastic scaling, managed runtime, pay-per-use.
- **Cons:** cold starts, limited long-lived state, vendor coupling, harder streaming and local
  Ollama integration.
- **Rejected:** conflicts with reproducible local development and local-inference evaluation.

### Single undifferentiated script

- **Pros:** minimal structure, fastest first demo.
- **Cons:** no provider substitution, no isolated tests, mixed business/provider concerns,
  difficult evaluation and security review.
- **Rejected:** the existing staged modules already demonstrate the cost of this approach.

### Off-the-shelf agent framework

- **Pros:** built-in orchestration, tool loops, tracing, and memory patterns.
- **Cons:** opaque control flow, framework lock-in, rapid API change, less explicit reasoning about
  trust and authority boundaries.
- **Rejected for this phase:** the project goal is an explicit, testable reference. This can be
  revisited if evaluation shows a framework advantage.

## Consequences

### Positive

- In-process calls keep latency and debugging simple.
- One repository and one process make setup, tests, evaluation, and incident reproduction easier.
- Provider and storage substitution happen at explicit interfaces.
- Business rules and approval gates are enforced in application code rather than by prompts.
- Layering gives future extraction a clear seam if scale or isolation demands it.

### Negative

- All capabilities share one failure domain and one deployment unit.
- Scaling is coarse-grained; SQLite has a single-writer limitation.
- Discipline is required to prevent SDK/config/storage imports from leaking into application and
  domain layers.
- A future split will require explicit contract and data-ownership work.

### Implementation obligations

1. Resolve the model-contract conflict (`Q-12`) and migrate all services to one contract.
2. Convert `src/ai_agent/config.py` and `src/ai_agent/config/` into an importable configuration
   package.
3. Inject the provider, prompt builder, tool registry/dispatcher, store, conversation manager, and
   memory manager from the composition root.
4. Remove `OpenAI`, `os.environ`, embedded prompt text, and registry construction from the
   orchestrator and classifier.
5. Add automated checks that domain never imports infrastructure and application never imports
   provider SDKs or storage SQL.
6. Keep provider, store, and approval behavior covered by fake-based tests.
7. Revisit this ADR when a review trigger in `architecture-decisions.md` fires.

### Current deviations

- `src/ai_agent/application/orchestrator.py:3,26-29` constructs `OpenAI` directly.
- `src/ai_agent/application/orchestrator.py:43,113` reads `OPENAI_MODEL` directly.
- `src/ai_agent/application/ticket_classifier.py:21-38` constructs `OpenAI` and reads the
  environment directly.
- `src/ai_agent/config.py` shadows the `config/` package.
- `src/ai_agent/application/model_client.py` conflicts with `src/ai_agent/domain/models.py`.

## Traceability

Supports `BR-01`, `BR-04`, `BR-10`, `BR-11`, `FR-01`, `FR-03`, `FR-04`, `FR-05`, `FR-06`,
`FR-10`, `FR-11`, `FR-14`, `NFR-09`, `NFR-11`, `NFR-13`.
