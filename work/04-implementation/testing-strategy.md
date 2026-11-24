# Testing Strategy

Status: Proposed · 2026-11-24

## Goals

- Verify behavior without live API keys or model calls.
- Catch contract regressions before provider/model changes reach evaluation.
- Prove safety rules with deterministic failure-injection tests.
- Keep the full suite green so evaluation results reflect the system, not broken imports.

## Test layers

| Layer | Scope | Tools / fixtures | Examples |
| --- | --- | --- | --- |
| Unit | Single function/class with fakes | pytest, fake `ModelClient`, injectable sleep | Retry backoff, prompt rendering, fact validation |
| Contract | Port conformance across implementations | Shared parameterized tests | OpenAI/Ollama produce same normalized result and errors |
| Integration | Several components with fake external edges | Temp SQLite DB, fake providers | Orchestrator → tools → store → context |
| Failure injection | Controlled errors/timeouts/limits | Fake clients/raisers | Refusal, rate limit, tool failure, context overflow, denied approval |
| Security | Trust boundaries and isolation | Temp DBs, fake identity, log capture | Owner isolation, secret redaction, untrusted-data handling |
| Evaluation | Model quality on a dataset | Versioned dataset and harness | Classification accuracy, JSON validity, groundedness |
| Static | Syntax/style/dependency rules | Ruff, proposed typechecker/dependency check | Undefined names, infrastructure imports in domain |

Unit/contract/integration tests are release-blocking. Evaluation is report-blocking for G3/G5.

## Current inventory

| Area | Test files |
| --- | --- |
| Root | `tests/test_assistant.py`, `tests/test_main.py` (empty), `tests/test_openai_provider.py`, `tests/test_prompt_builder.py` |
| Application | `test_context_manager.py`, `test_conversation_manager.py`, `test_conversation_store.py`, `test_generation_options.py`, `test_memory_extractor.py`, `test_memory_manager.py`, `test_memory_retriever.py`, `test_model_registry.py`, `test_model_selection.py`, `test_retry.py`, `test_streaming.py`, `test_ticket_validation.py` |
| Domain | `test_memory.py`, `test_ticket_classification.py` |
| Prompts | `test_prompt_builder.py`, `test_prompt_registry.py`, `test_prompt_template.py` |
| Tools | `test_order_tools.py`, `test_tool_dispatcher.py`, `test_tool_executor.py`, `test_tool_registry.py` |

`tests/conftest.py` sets dummy `OPENAI_API_KEY` and `OPENAI_MODEL`. Conversation/memory tests use
temporary SQLite databases and fakes.

## Current baseline

- `uv run pytest -q` fails during collection on `Iterator` in `OpenAIProvider.stream()` and
  `LLMValidationError` in `ticket_validation.py`.
- 57 tests pass when those two modules are excluded.
- `uv run ruff check .` reports 8 errors.
- No CI, typechecker, coverage report, or live-provider integration suite exists.

## Required test additions

| Area | Tests to add | Traces |
| --- | --- | --- |
| Configuration | Missing/invalid variables, import of profiles/catalog, no secret in errors | `FR-10`, `NFR-05` |
| Model contract | Canonical generate/stream/structured result behavior with fakes | `FR-02`, `FR-07`, `FR-10` |
| Providers | OpenAI stream events and errors; Ollama mocked generate/stream; usage normalization | `FR-07`, `FR-10` |
| Provider factory | Selection, unknown provider, capability check, fallback policy | `FR-10`, `FR-13` |
| Classification | Success, refusal, incomplete, malformed JSON, extra field, invalid business value, retry/exhaustion | `FR-02`, `FR-12` |
| Orchestrator | Success, turn limit, tool-call limit, unknown tool, provider error, denied approval | `FR-03`, `FR-04`, `FR-09` |
| Tools | Allowlist, strict args, malformed JSON, handler error, no execution on denial | `FR-03`, `FR-14` |
| Conversation/memory | Persistence restart, context order, budget eviction, owner isolation, correction upsert | `FR-05`, `FR-06` |
| Generation/selection | Option omission, explicit zero, unknown task/model, profile mapping | `FR-08`, `FR-13` |
| Streaming | Chunk order, cancellation, timeout, bounded buffer, partial JSON rejected | `FR-07`, `NFR-03` |
| Error mapping | SDK exceptions → taxonomy; sanitized messages; retry decisions | `FR-12`, `NFR-07` |
| CLI | Configurable input, friendly errors, exit codes, no hardcoded ticket | `FR-01`, `FR-15` |
| Observability | Trace ID, required fields, secret/sensitive-content redaction | `FR-15`, `NFR-13` |
| Architecture rules | Domain has no provider/DB/web imports; application has no SDK/env reads | `NFR-09` |

## Failure-injection matrix

| Failure | Injection point | Expected behavior |
| --- | --- | --- |
| Authentication error | Fake provider raises classified auth error | Permanent failure, sanitized message, no retry |
| Rate limit | Fake provider raises `LLMRateLimitError(retry_after=...)` | Honors `retry_after`, bounded attempts |
| Timeout | Fake provider raises `LLMTimeoutError` | Retries within budget, then controlled failure |
| Invalid JSON | Fake provider returns malformed text | `LLMParsingError`/response error, no guessed result |
| Refusal | Fake response includes refusal content | `LLMRefusalError`, controlled fallback |
| Incomplete response | Fake status `"incomplete"` | `LLMIncompleteResponseError`, no parse |
| Unknown tool | Model requests unregistered tool | Rejected before dispatcher handler |
| Invalid tool arguments | Extra/missing/wrong-type fields | `ToolExecutionError`, no handler call |
| Tool handler failure | Fake handler raises | Classified tool error, sanitized `ToolResult` |
| Context overflow | Oversized system/message facts | `ContextWindowExceeded`, explicit failure |
| Cross-owner access | Query with mismatched owner | No rows/denial; audit event without sensitive content |
| Denied approval | Approver denies consequential action | No tool execution; decision recorded |

## Fakes and fixtures

- **FakeModelClient:** configurable text/chunks/status/errors/usage; records requests.
- **FakeApprover:** approves/denies and records decisions.
- **Temporary store:** unique temp SQLite path per test; cleaned up after test.
- **Injectable sleep:** `execute_with_retry(..., sleep=fake_sleep)` prevents real delays.
- **Dummy settings:** from `tests/conftest.py`; never real keys.
- **No live network:** unit/contract/integration suites must pass offline.

## Commands

| Command | Use |
| --- | --- |
| `uv run pytest -q` | Full suite; must pass in CI |
| `uv run pytest tests/application/test_streaming.py -q` | Focused streaming check during refactor |
| `uv run pytest -q -k "<pattern>"` | Focused subset during development |
| `uv run ruff check .` | Full lint; must pass in CI |
| `uv run ruff check <path>` | Changed-path lint before commit |

Do not permanently exclude broken modules from the suite; fix the import/runtime error.

## CI sequence

1. `uv sync --frozen` (or equivalent locked install).
2. `uv run ruff check .`
3. `uv run pytest -q`
4. Proposed typechecker and dependency-boundary check when configured.
5. Evaluation report job when dataset/harness exists.
6. Publish test/lint/evaluation artifacts as gate evidence.

## Definition of done

A test suite change is complete when:

- the test fails for the intended reason before the fix and passes after it;
- no real credentials, network, or local model runtime are required;
- error messages and logs are asserted not to contain secrets or sensitive content;
- the relevant spec/trace ID is updated;
- CI runs the test on every change.

## Traceability

Supports `BR-09`, `FR-12`, `FR-13`, `FR-14`, `FR-15`, `NFR-01`, `NFR-06`, `NFR-07`, `NFR-12`,
`NFR-13`, and the exit gates in `../01-discovery/success-metrics.md`.
