# Metrics

Status: Target metric contract · No exporter exists today

## Current state

Token counts are computed in `OpenAIProvider` and printed by `src/ai_agent/main.py`. There are no
counters, histograms, gauges, exporters, labels, recording rules, or metric-backed alerts. Model,
classification, tool, retry, approval, and migration outcomes are unmeasured.

## Metric contract

| Rule | Value |
| --- | --- |
| Naming | Lowercase snake_case; unit suffix where useful (`_ms`, `_tokens`, `_total`) |
| Types | Counter, histogram, gauge |
| Required labels | `environment`, `service`, `revision`, `provider`, `model` where applicable |
| Optional labels | `profile`, `category`, `tool_name`, `outcome`, `error_class`, `channel` |
| Forbidden labels | Raw owner/customer IDs, ticket text, prompt/output content, secret values |
| Units | Tokens as integers; latency in milliseconds; cost in reporting currency minor units or documented currency |
| Missing value | Report `unmeasured`; never emit zero for an unimplemented check |
| Cardinality | Approved enums only; no unbounded IDs or free text |

## Operational catalog

| Metric | Type | Labels | Source | Related target |
| --- | --- | --- | --- | --- |
| `tickets_total` | Counter | outcome, category, channel | Request/ticket adapter | M-03, M-05 |
| `ticket_duration_ms` | Histogram | outcome, profile, model | Request timestamps | M-05, M-06 |
| `classification_duration_ms` | Histogram | category, outcome | Classifier | M-05 |
| `classification_correct_total` | Counter | category, dataset_version | Evaluation labels | M-01 |
| `structured_output_valid_total` | Counter | outcome, error_class | Parser/validator | M-02 |
| `first_token_duration_ms` | Histogram | provider, model | Stream adapter | M-07 |
| `model_tokens_total` | Counter | direction (`input`/`output`/`cached`), provider, model, profile | Provider usage | M-08 |
| `model_calls_total` | Counter | outcome, error_class, finish_reason | Model port | M-10 |
| `retry_attempts_total` | Counter | operation, error_class | Retry helper | M-10 |
| `tool_calls_total` | Counter | tool_name, outcome, validation_result | Tool dispatcher | M-04 |
| `approval_decisions_total` | Counter | decision, requester_role, approver_role | Approval gate | M-12 |
| `authorization_denials_total` | Counter | control, reason | Security controls | M-11 |
| `owner_isolation_violations_total` | Counter | test/suite | Isolation tests/audit | M-11 |
| `context_tokens_total` | Counter | action (`retained`/`dropped`), source | Context manager | M-08 |
| `memory_operations_total` | Counter | operation, outcome, owner_match | Memory manager/store | M-03, M-11 |
| `provider_errors_total` | Counter | provider, error_class, retried | Provider adapter | M-10 |
| `estimated_cost_minor_units` | Counter | provider, model, environment, revision | Usage × approved prices | M-09 |
| `migration_duration_ms` | Histogram | version, outcome | Migration runner | Release gate |
| `tests_passed_total` / `tests_failed_total` | Counter | suite, revision | CI | M-13 |
| `lint_findings_total` | Gauge | revision | CI | M-14 |
| `adr_documentation_coverage_ratio` | Gauge | revision | Doc review | M-15 |

## Discovery metric mapping

| ID | Operational source | Report cadence |
| --- | --- | --- |
| M-01 | `classification_correct_total` over labeled dataset | Per evaluation run |
| M-02 | `structured_output_valid_total` over parsed outputs | Per evaluation run and live |
| M-03 | Human-review labels linked by `trace_id` | Per evaluation batch |
| M-04 | `tool_calls_total` outcomes on scenario set | Per evaluation and live |
| M-05 | `ticket_duration_ms` average | Live dashboard + evaluation |
| M-06 | `ticket_duration_ms` P95 | Live dashboard + evaluation |
| M-07 | `first_token_duration_ms` | Streaming evaluation |
| M-08 | `model_tokens_total` | Live + evaluation |
| M-09 | `estimated_cost_minor_units` + infra allocation | Daily/monthly |
| M-10 | `retry_attempts_total`, `provider_errors_total`, `model_calls_total` | Live |
| M-11 | `authorization_denials_total`, `owner_isolation_violations_total` | Live/test |
| M-12 | `approval_decisions_total` | Live/test |
| M-13 / M-14 / M-15 | CI/doc review metrics | Per release |

## Runtime and evaluation separation

- Runtime metrics describe actual traffic and may be aggregated by approved low-cardinality labels.
- Evaluation metrics are produced by the frozen harness and include dataset version and holdout
  split; they are not inferred from production logs.
- Release evidence links both to the same code revision and configuration.
- A metric without provider, model, prompt/profile version, context limits, retry policy, date,
  and code revision is an estimate, not a result (`../01-discovery/success-metrics.md`).

## Recording and exposition

- Counters are monotonic; histograms record bucketed values for P95 calculation.
- Gauges represent current state (lint findings, documentation coverage, active releases).
- Exemplars carry `trace_id` where supported.
- Metric emission is non-blocking and must never fail a ticket response.
- Missing price/config data blocks cost reporting; it does not default to zero cost.
- Metric endpoints are internal/redacted; no customer payloads in labels or help text.

## Verification

- Unit tests assert one metric event per model call, tool call, retry, and approval decision.
- Label allowlist test rejects free text/secret-like values.
- Known fake secret injected into provider error is absent from metric labels.
- Token totals reconcile with provider usage records in evaluation runs.
- Cost estimate reconciles with approved price table and retries.
- Histogram P95 matches a fixed sample within agreed tolerance.
- Dashboard/alert queries tested against fixtures with unmeasured values.

## Traceability

Supports M-01–M-15, `BR-09`, `FR-15`, `NFR-08`, `NFR-12`, and `../08-operations/logging.md`.
