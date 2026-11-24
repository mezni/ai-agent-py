# Implementation Plan

Status: Proposed sequence · 2026-11-24

## Goals

1. Restore a trustworthy baseline: full test collection, lint, and reproducible setup.
2. Establish one canonical model contract and inject all collaborators from a composition root.
3. Deliver an end-to-end, tool-grounded support answer with validated structured classification.
4. Integrate conversation, memory, streaming, approval, and observability behind stable interfaces.
5. Produce measured evaluation evidence and enforce release gates.

## Non-goals

- Training/fine-tuning models or building an authoritative business system.
- Building a full customer-facing UI before the core flow is verified.
- Splitting into microservices (`ADR-001`).
- Treating mock order/customer/FAQ data as production data.

## Phase overview

| Phase | Name | Primary outcome | Gate |
| --- | --- | --- | --- |
| P0 | Restore baseline | Tests collect, lint errors understood/fixed, config importable | G2 foundation |
| P1 | Contract and composition | One model contract; provider and collaborators injected | G2 foundation |
| P2 | Provider parity | OpenAI and Ollama adapters satisfy the same contract | G3 evaluation prep |
| P3 | Classification and output | Structured, validated, provider-neutral classification | G3 evaluation prep |
| P4 | Tools and orchestration | Bounded tool loop with approval and classified errors | G4 safety |
| P5 | Conversation and memory | Multi-turn context with owner-scoped facts | G4 safety |
| P6 | Streaming and resilience | Safe chunks, timeouts, cancellation, telemetry | G3/G4 evidence |
| P7 | Evaluation and release | Dataset, harness, reports, quality gates, sign-off | G5 acceptance |

## P0 — Restore baseline

**Why first:** no later change can be trusted while full test collection fails and configuration
cannot import its catalogs.

**Tasks**

- Import `Iterator` and implement a valid `OpenAIProvider.stream()` or temporarily remove the
  broken annotation and track it explicitly.
- Define `LLMValidationError` in `application/errors.py` and extend the taxonomy consistently.
- Resolve `config.py` vs. `config/` shadowing by converting configuration to a package.
- Declare the `ollama` dependency or guard the optional import until P2.
- Record the baseline result of `uv run pytest -q` and `uv run ruff check .`.

**Exit criteria**

- Full pytest collection succeeds and the passing test count is recorded.
- Ruff findings are zero or each remaining finding has an owner and waiver.
- Generation profiles and model catalog import successfully.
- `ADR-004` decision on the canonical contract is started or recorded.

**Traces:** `FR-15`, `NFR-11`, `NFR-12`, `ADR-003`.

## P1 — Contract and composition

**Tasks**

- Decide and document the canonical model contract (`Q-12`, pending `ADR-004`).
- Migrate `CustomerSupportAssistant`, `Assistant`, classifier, summarizer, and orchestrator to it.
- Add a provider factory selected from validated settings.
- Move provider, prompt, registry, dispatcher, store, conversation, and memory construction into
  `main.py` or a dedicated composition module.
- Remove SDK imports and environment reads from application modules.

**Exit criteria**

- Application tests run with fake providers and no live keys.
- Switching provider configuration requires no application-code edit.
- Architecture/dependency checks show domain has no infrastructure imports.

**Traces:** `FR-02`, `FR-04`, `FR-10`, `NFR-09`, `ADR-001`.

## P2 — Provider parity

**Tasks**

- Complete OpenAI streaming event iteration, error normalization, and usage capture.
- Add declared `ollama` dependency and mocked Ollama generate/stream tests.
- Map generation options centrally; omit `None`, preserve explicit zero.
- Verify capability flags and context windows against provider documentation.
- Add fallback policy when a configured provider is unavailable.

**Exit criteria**

- Both adapters pass the same contract suite.
- Local provider imports and tests pass without a running Ollama runtime.
- Capability checks are based on documented values, not placeholders.

**Traces:** `FR-07`, `FR-08`, `FR-10`, `FR-13`, `NFR-03`, `NFR-14`.

## P3 — Classification and structured output

**Tasks**

- Inject prompt registry/builder, parser, validator, and retry policy into the classifier.
- Use the agreed prompt version and strict `TicketClassification` schema.
- Add tests for refusal, incomplete status, malformed output, extra fields, invalid business
  values, retry success, and retry exhaustion.
- Ensure only complete responses produce classification values.

**Exit criteria**

- Classifier has no provider SDK or environment dependency.
- Structured-output validity and classification accuracy are measured on the evaluation dataset.
- Partial streamed JSON cannot become a classification result.

**Traces:** `FR-02`, `FR-08`, `FR-12`, `FR-13`, `NFR-01`, `ADR-002`, `ADR-003`.

## P4 — Tools and orchestration

**Tasks**

- Inject tool registry and dispatcher into the orchestrator.
- Move embedded prompt text into the prompt registry.
- Keep the 5-turn / 10-tool-call limits configurable.
- Classify tool errors and sanitize messages; remove broad `except Exception`.
- Add the consequential-action approval gate and an approval record.
- Add owner/permission checks before protected tool execution.

**Exit criteria**

- Unknown tools and invalid arguments never reach handlers.
- Tool results are labeled as data and cannot override system instructions.
- No consequential action executes without an approval decision.

**Traces:** `FR-03`, `FR-04`, `FR-09`, `FR-12`, `FR-14`, `NFR-06`, `NFR-07`.

## P5 — Conversation and memory

**Tasks**

- Add `owner_id` to conversations and scope store queries.
- Wire `ConversationManager`, `ContextManager`, and `MemoryManager` into the orchestrator.
- Assemble context in the target order: system, long-term facts, summary, recent history, current
  request.
- Add automatic summarization triggers and owner-correction behavior.
- Add owner-isolation tests across read, upsert, and delete.

**Exit criteria**

- Multi-turn scenario passes without live API calls.
- No cross-owner read or write is possible.
- History and memory are never treated as authoritative business state.

**Traces:** `FR-05`, `FR-06`, `FR-14`, `BR-07`, `BR-08`, `NFR-06`.

## P6 — Streaming and resilience

**Tasks**

- Implement cancellation, connection/read timeouts, bounded buffers, and sanitized errors.
- Add TTFT/completion metrics and non-sensitive logs.
- Apply one retry/error policy across classifier, providers, and orchestrator.
- Add failure-injection tests for timeout, rate limit, malformed JSON, tool failure, and context
  overflow.

**Exit criteria**

- Streaming path passes contract and load checks.
- Failures produce controlled, user-appropriate results without leaking provider details.
- Observability fields are present on every model/tool call.

**Traces:** `FR-07`, `FR-12`, `FR-15`, `NFR-02`, `NFR-03`, `NFR-07`, `NFR-13`.

## P7 — Evaluation and release

**Tasks**

- Freeze dataset version, prompt version, model ID, generation profile, tool schemas, and context
  settings.
- Run the evaluation harness for cloud and local candidates.
- Report M-01–M-12 from `../01-discovery/success-metrics.md` with confidence intervals and failure
  examples.
- Enforce `quality-gates.md` in CI and complete `release-checklist.md`.

**Exit criteria**

- G3–G5 exit criteria are met or explicitly waived by the owner.
- Evaluation report includes reproducibility metadata.
- Release decision is recorded with evidence.

**Traces:** `BR-09`, `FR-13`, `FR-15`, `NFR-01`, `NFR-04`, `NFR-12`.

## Dependencies and parallel work

| Can run in parallel | Requires first |
| --- | --- |
| Error taxonomy fix and config package fix | P0 start |
| OpenAI stream fix and Ollama dependency/tests | P1 contract decision |
| Prompt migration and tool/approval design | P1 composition root |
| Dataset authoring and harness design | P0 baseline; can start early |

Do not wire conversation/memory into the orchestrator before the contract and composition root are
stable; doing so would multiply the interface conflict.

## Risk controls

| Risk | Control |
| --- | --- |
| Contract change breaks many callers | One decision ADR, small migration commits, fake-based contract tests |
| Tests stay red while features are added | P0 gate blocks later phases |
| Local provider blocks evaluation | Guard optional import; mock in tests; add dependency in P2 |
| Security gap discovered late | Run G4 safety checks before acceptance, not after |
| Unmeasured quality targets become assumptions | P7 report with explicit reproducibility metadata |
