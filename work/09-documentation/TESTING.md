# Testing

Status: Strategy and current baseline · 2026-11-24

## Goals

- Verify behavior without live API keys or model runtimes.
- Catch contract regressions before provider/model changes reach evaluation.
- Prove safety with deterministic failure-injection tests.
- Keep the full suite green so evaluation results describe the system, not broken imports.

## Current baseline

| Check | Result |
| --- | --- |
| `uv run pytest -q` | Fails collection on `Iterator` and `LLMValidationError` |
| Tests when broken modules excluded | 57 pass |
| `uv run ruff check .` | 8 pre-existing errors |
| CI / typechecker / coverage | None configured |
| Live-provider integration suite | None |
| Evaluation dataset/harness | Not created |

`uv run pytest tests/application/test_streaming.py -q` reports 2 passing tests. Unit and
conversation tests use fakes and temporary SQLite databases; `tests/conftest.py` sets dummy
`OPENAI_API_KEY` and `OPENAI_MODEL`.

## Test layers

| Layer | Scope | Examples |
| --- | --- | --- |
| Unit | One function/class with fakes | Retry backoff, prompt rendering, fact validation |
| Contract | Port conformance across providers | Generate/stream/usage/error normalization |
| Integration | Several components; fake external edges | Orchestrator → tools → store → context |
| Failure injection | Controlled errors/timeouts/limits | Refusal, rate limit, tool failure, context overflow, denied approval |
| Security | Trust boundaries and isolation | Owner isolation, redaction, untrusted-data handling |
| Evaluation | Model quality on frozen dataset | M-01–M-12; not yet implemented |
| Static | Style/dependency rules | Ruff; proposed typechecker/architecture checks |

Unit, contract, integration, and security tests are release-blocking. Evaluation is report-blocking
for G3/G5 in `../01-discovery/success-metrics.md`.

## Current inventory

| Area | Test files |
| --- | --- |
| Root | `test_assistant.py`, `test_main.py` (empty), `test_openai_provider.py`, `test_prompt_builder.py` |
| Application | context/conversation/store, generation options, memory extractor/manager/retriever, model registry/selection, retry, streaming, ticket validation |
| Domain | `test_memory.py`, `test_ticket_classification.py` |
| Prompts | `test_prompt_builder.py`, `test_prompt_registry.py`, `test_prompt_template.py` |
| Tools | `test_order_tools.py`, `test_tool_dispatcher.py`, `test_tool_executor.py`, `test_tool_registry.py` |

## Required additions

| Area | Tests to add |
| --- | --- |
| Configuration | Missing/invalid variables, profile/catalog imports, no secret echoed |
| Model contract | Canonical generate/stream/structured behavior with fakes (`ADR-004`) |
| Providers | OpenAI stream events/errors; mocked Ollama generate/stream; usage normalization |
| Provider factory | Selection, unknown provider, capability check, fallback policy |
| Classification | Success, refusal, incomplete, malformed JSON, extra field, invalid value, retry exhaustion |
| Orchestrator | Success, turn/tool limits, unknown tool, provider error, denied approval |
| Tools | Allowlist, strict args, malformed JSON, handler failure, no execution on denial |
| Conversation/memory | Restart persistence, context order, budget eviction, owner isolation, correction upsert |
| Generation/selection | Option omission, explicit zero, unknown task/model, profile mapping |
| Streaming | Chunk order, cancellation, timeout, bounded buffer, partial JSON rejected |
| Error mapping | SDK exceptions → taxonomy; sanitized messages; retry decisions |
| CLI | Configurable input, friendly errors, exit codes, no hardcoded ticket |
| Observability | Trace ID, required fields, secret/sensitive-content redaction |
| Architecture rules | Domain has no provider/DB/web imports; application has no SDK/env reads |

## Failure-injection rules

| Failure | Expected |
| --- | --- |
| Authentication error | Permanent failure, sanitized message, no retry |
| Rate limit | Honors `retry_after`, bounded attempts |
| Timeout/connection | Retries within budget then controlled failure |
| Invalid/incomplete/refused output | Distinct classified error; no guessed result |
| Unknown/invalid tool | Rejected before handler call |
| Handler failure | Classified tool error with sanitized result |
| Context overflow | `ContextWindowExceeded`, explicit failure |
| Cross-owner access | No rows/denial plus redacted audit event |
| Missing approval | Consequential action not executed |

## Release gates

| Gate | Requirement |
| --- | --- |
| G2 | Full tests + lint pass; config importable; canonical contract chosen |
| G3 | Frozen dataset; M-01–M-10 reported for cloud and local candidates |
| G4 | Owner isolation, approval, untrusted-data handling, and redaction tests pass |
| G5 | M-01–M-12 thresholds met on holdout data; docs/ADRs current |

“Unmeasured” does not pass a gate. Waivers require owner, requirement, expiry, and mitigation.

## Commands and evidence

- Run focused tests during development; run the full suite before review.
- Record test/lint output in the PR or release record.
- Never attach raw prompts, model outputs, customer data, or secrets to test artifacts.
- Evaluation reports must record dataset/prompt/model/profile/context/retry/code versions.

## Traceability

Summarizes `../04-implementation/testing-strategy.md`, `quality-gates.md`, and M-13/M-14 in
`../01-discovery/success-metrics.md`.
