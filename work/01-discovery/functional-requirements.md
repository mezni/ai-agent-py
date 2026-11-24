# Functional Requirements

Status: Proposed · 2026-11-24

Status values describe the repository at discovery time: **Observed** (working behavior present),
**Partial** (code exists but incomplete or unwired), or **Planned** (not implemented).

## FR-01 — Run a support assistant from the CLI

**Priority:** Must · **Status:** Partial · **Traces:** BR-01

The entry point accepts a support message and returns a response with usage information.

**Acceptance criteria**

- A user can run the installed `ai-agent-py` command after `uv sync` and configuration.
- The message is no longer hardcoded; it can be supplied by argument or interactive input.
- Response, model, token usage, and error outcome are visible to the operator.
- Missing configuration produces an actionable error instead of an import-time `KeyError`.

**Evidence:** `src/ai_agent/main.py`, `README.md:10-36`, `src/ai_agent/config.py`.

## FR-02 — Classify a ticket with validated structured output

**Priority:** Must · **Status:** Partial · **Traces:** BR-02

The system classifies a ticket into agreed categories and returns a schema-valid result.

**Acceptance criteria**

- Output is parsed only after the complete response is received and status is confirmed.
- Refusals, incomplete responses, malformed JSON, and invalid business values are distinct
  failure paths.
- Classification uses low-variation generation settings with a controlled output budget.
- The canonical model-client contract is used; no provider SDK is called by the classifier.

**Evidence:** `src/ai_agent/application/ticket_classifier.py`, `response_parser.py`,
`ticket_validation.py`, `tests/domain/test_ticket_classification.py`, `README.md:157-188`.

## FR-03 — Ground answers in allowlisted tools

**Priority:** Must · **Status:** Partial · **Traces:** BR-01, BR-04

The agent may call only registered tools for authoritative order, customer, and FAQ data.

**Acceptance criteria**

- Every tool call is checked against an allowlist and validated against a strict argument schema.
- Unknown tools and extra/invalid arguments are rejected before handler execution.
- Tool results are passed to the model as data, not instructions.
- Each answer can be associated with the tool facts used.

**Evidence:** `src/ai_agent/tools/tool_registry.py`, `tool_dispatcher.py`, `schemas.py`,
`src/ai_agent/application/orchestrator.py:50-55`.

## FR-04 — Coordinate a bounded tool-use conversation

**Priority:** Must · **Status:** Partial · **Traces:** BR-01, BR-07

An orchestrator coordinates prompt → model → parse → validate → tool → result within explicit
limits.

**Acceptance criteria**

- Maximum turns and tool calls are configurable; defaults are 5 turns and 10 tool calls.
- Dependencies (model client, prompt builder, parser, validator, tool dispatcher) are injected.
- The orchestrator does not create provider SDK clients, read keys, embed provider logic, or
  access storage directly.
- Unit tests use fakes and cover success, loop-limit, invalid-tool-output, and provider-error cases.

**Evidence:** `src/ai_agent/application/orchestrator.py`, `README.md:267-294`.

## FR-05 — Persist and assemble conversation state

**Priority:** Should · **Status:** Partial · **Traces:** BR-07, BR-08

The system stores conversations, messages, and memory, and builds model-ready context.

**Acceptance criteria**

- Conversation, message, and memory records persist across process restarts.
- Context order is system instructions, relevant long-term facts, summary, recent history, and
  current request.
- Token budget and response reserve are enforced; fixed content that cannot fit raises a clear
  error.
- Owner IDs used for storage and retrieval come from authenticated application context.

**Evidence:** `src/ai_agent/application/conversation_store.py`, `conversation_manager.py`,
`context_manager.py`, `README.md:60-98`.

## FR-06 — Use owner-scoped long-term memory

**Priority:** Should · **Status:** Partial · **Traces:** BR-07, BR-08

The system summarizes, extracts, stores, and retrieves facts scoped to an owner.

**Acceptance criteria**

- Facts validate owner, key, confidence, source, and timestamp.
- Repeated facts update the existing key; corrections replace stale values.
- Retrieved memory is labeled as supporting context and treated as untrusted data.
- Automatic summarization triggers and retrieval are integrated into context assembly.
- Owner isolation tests prove no cross-owner read, update, or delete.

**Evidence:** `src/ai_agent/domain/memory.py`, `src/ai_agent/application/memory_*.py`,
`README.md:100-127`.

## FR-07 — Stream assistant responses

**Priority:** Should · **Status:** Partial · **Traces:** BR-01, BR-12

The user can receive generated text incrementally while the complete response remains the only
trusted result for structured processing.

**Acceptance criteria**

- The provider iterates stream events and yields text chunks without undefined names.
- Streaming uses the canonical model-client contract and preserves the non-streaming path.
- Cancellation, connection/read timeouts, bounded buffers, and sanitized errors are implemented.
- Time to first token and completion are observable; logs avoid sensitive generated content.
- Partially streamed JSON is never parsed as a classification result.

**Evidence:** `src/ai_agent/application/model_client.py`,
`src/ai_agent/providers/openai_provider.py`, `tests/application/test_streaming.py`,
`README.md:129-155`.

## FR-08 — Select and configure generation parameters by task

**Priority:** Should · **Status:** Partial · **Traces:** BR-02, BR-10

Task profiles choose frozen generation settings, and the provider maps them to API options.

**Acceptance criteria**

- Profiles are importable and cover classification, extraction, customer response, and RAG.
- `None` values are omitted; explicit zero values are preserved.
- Response status and completion are checked before parsing a budget-limited JSON response.
- Profile choices are backed by repeated trials on a representative dataset.

**Evidence:** `src/ai_agent/application/generation_config.py`, `generation_options.py`,
`src/ai_agent/config/generation_profiles.py`, `README.md:157-188`.

## FR-09 — Require human approval for consequential actions

**Priority:** Must · **Status:** Planned · **Traces:** BR-03, BR-08

Consequential actions are proposed by the agent but executed only after explicit human approval.

**Acceptance criteria**

- An agreed action list is classified as consequential.
- Approval records the approver, action, arguments, timestamp, and decision.
- Unapproved or denied actions cannot reach tool execution.
- The system remains usable when approval is unavailable or denied.

**Evidence:** `README.md:208-210`, `README.md:279-281`.

## FR-10 — Abstract and select model providers

**Priority:** Must · **Status:** Partial · **Traces:** BR-06, BR-10

One canonical model-client interface is implemented by cloud and local adapters and selected by
configuration.

**Acceptance criteria**

- A provider factory selects the provider from configuration without application code changes.
- OpenAI and Ollama adapters share the same contract and pass the same contract tests.
- Provider-specific request mapping, error normalization, and stream events stay in adapters.
- Provider capabilities and context limits are verified against documentation, not placeholders.

**Evidence:** `README.md:228-263, 267-294`, `src/ai_agent/providers/**`.

## FR-11 — Version prompts and registrations

**Priority:** Should · **Status:** Observed · **Traces:** BR-10, BR-11

Prompts, prompts registry entries, tools, and models are centrally registered and versioned.

**Acceptance criteria**

- Duplicate registrations are rejected with clear errors.
- The active prompt version and tool/model catalog entries are explicit.
- Prompt or catalog changes are reviewable and traceable to evaluation results.

**Evidence:** `src/ai_agent/prompts/**`, `src/ai_agent/tools/tool_registry.py`,
`src/ai_agent/application/model_registry.py`.

## FR-12 — Classify and recover from failures

**Priority:** Must · **Status:** Partial · **Traces:** BR-02, BR-12

Errors are classified and handled according to retryability and user impact.

**Acceptance criteria**

- Timeout, rate limit, transient provider, invalid response, tool, and authorization errors are
  distinguishable.
- Retries use bounded attempts, jitter/backoff, and an injectable sleep for tests.
- Retry behavior is consistent across classifier, provider, and orchestrator paths.
- Non-retryable failures return a controlled result without exposing provider internals.

**Evidence:** `src/ai_agent/application/errors.py`, `retry.py`, `README.md:143-155`.

## FR-13 — Evaluate and compare models

**Priority:** Must · **Status:** Partial · **Traces:** BR-05, BR-06, BR-09

Models and profiles are compared on the same representative dataset before selection.

**Acceptance criteria**

- A versioned dataset and evaluation script report accuracy, JSON validity, completion, latency,
  token usage, cost, and tool-call correctness.
- Cloud and local comparisons also report average/P95 latency and RAM/VRAM usage.
- Results are recorded as measurements, not hypothetical tables.
- Selection is configurable and includes fallback and observability.

**Evidence:** `README.md:190-226, 253-255`, `src/ai_agent/application/model_selection.py`.

## FR-14 — Enforce security boundaries in the workflow

**Priority:** Must · **Status:** Partial · **Traces:** BR-08, BR-12

Security rules are enforced in application code, not left to model instructions.

**Acceptance criteria**

- Secrets come from environment/configuration and are never logged or committed.
- `owner_id` is derived from authenticated context; all storage queries are owner-scoped.
- Tool results, memory, summaries, and retrieved documents are untrusted data.
- Consequential actions and access to protected tools require authorization.
- Logs and traces redact keys, tokens, and sensitive customer content.

**Evidence:** `README.md:23, 94-95, 116-118, 255-256`, `src/ai_agent/application/conversation_store.py`.

## FR-15 — Provide reproducible verification and observability

**Priority:** Must · **Status:** Partial · **Traces:** BR-09

Tests, lint, and telemetry give reliable evidence about the current build.

**Acceptance criteria**

- Full pytest collection succeeds and the suite passes with fake providers.
- Ruff passes; no undefined names or unresolved imports remain.
- Metrics include latency, token usage, cost, tool failures, retries, and approval decisions.
- CI runs verification on every change and records the results.

**Evidence:** `README.md:25-33, 313-320`, `pyproject.toml:26-34`, `tests/**`.
