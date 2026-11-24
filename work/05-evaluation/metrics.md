# Evaluation Metrics

Status: Metric definitions · Proposed targets · 2026-11-24

Targets come from `../01-discovery/success-metrics.md`. No model quality, latency, or cost result has
been measured. “Unmeasured” must never be reported as zero, pass, or not applicable.

## Reporting metadata

Every metric report must record:

- dataset version + SHA-256 + split;
- code revision, release candidate;
- provider, model, prompt name/version, schema version, generation profile;
- tool versions, context limits, response reserve, retry policy, temperature/top-p/token caps;
- price-table version and currency where cost is reported;
- date, operator, harness version, repetitions, and confidence method;
- trace IDs for sampled successes and all failures.

## Definitions

| ID | Metric | Formula / method | Source | Target |
| --- | --- | --- | --- | --- |
| M-01 | Classification accuracy | `correct_category / cases_with_valid_classification`; report invalid/failed cases separately | Labeled dataset + parsed result | ≥95% proposed |
| M-02 | Structured-output validity | `cases_passing_status+parse+schema+business_rules / attempted_cases` | Parser/validator outcomes | ≥99% proposed |
| M-03 | Response correctness/groundedness | Human rubric score and tool-fact attribution per case; report pass rate + disagreements | Review labels + trace IDs | Owner threshold pending |
| M-04 | Tool-call success rate | `correct_tool+valid_args+expected_result / cases_requiring_tools` | Expected vs actual tool calls | Owner threshold pending |
| M-05 | Average end-to-end latency | Mean(request receipt → complete response) in ms | Timestamps/traces | <2 s proposed |
| M-06 | P95 end-to-end latency | 95th percentile of same durations | Latency histogram | Owner threshold pending |
| M-07 | TTFT | First streamed chunk timestamp − request receipt; only streaming cases | Stream events | Owner threshold pending |
| M-08 | Token usage per ticket | Mean and distribution of input/output/cached tokens | Provider usage records | Within cost model |
| M-09 | Cost per ticket / month | Usage × versioned prices + retries + infra/storage/obs allocation; monthly extrapolation at agreed volume | Cost report | Approved budget pending |
| M-10 | Retry and failure rate | `retry_attempts / calls`, `terminal_failures / cases`, by error class | Retry/error telemetry | Agreed error budget pending |
| M-11 | Owner-isolation violations | Count of cross-owner reads/writes/deletes | Security tests/audit | 0 |
| M-12 | Unapproved consequential actions | Count of consequential actions executed without recorded approval | Approval audit | 0 |
| M-13 | Test pass rate | Passing selected tests / selected tests; separate collection errors | CI test log | 100% |
| M-14 | Lint findings | Count from `uv run ruff check .` | CI lint log | 0 |
| M-15 | Documentation/decision coverage | Significant decisions with ADRs / significant decisions; review checklist | ADR index/docs review | All significant decisions |

## Inclusion and exclusion rules

- Denominator for M-01 includes only cases with a valid final classification; invalid/failed cases
  are counted in M-02/M-10 and listed, never hidden.
- Empty-ticket cases are controlled validation cases; they do not enter M-01 denominator.
- Injection cases enter M-01/M-02 only when a valid result is produced; they always enter safety
  reporting.
- Retry cases count each attempt for M-08/M-09/M-10 but one final outcome for M-01/M-02.
- Holdout results are reported separately from dev results; never average them together for gate
  decisions.
- Candidate comparisons use identical dataset, prompt, profile, context limits, retry policy, and
  repetitions; differences must be recorded.

## Instrumentation needs

| Metric | Instrumentation status |
| --- | --- |
| M-01/M-02 | Parser/validator outcomes exist as code paths; harness not implemented |
| M-03 | No human-review workflow or trace links yet |
| M-04 | Tool result model exists; no scenario harness |
| M-05/M-06/M-07 | No request timestamps/stream events exported |
| M-08 | Provider token counts printed by CLI; no exporter |
| M-09 | No price table or cost report |
| M-10 | Error taxonomy/retry helper exist; no telemetry |
| M-11/M-12 | No auth or approval gate; tests not implemented |
| M-13/M-14 | Commands available; baseline failing |
| M-15 | ADR index exists; design/evaluation packs partial at discovery |

## Aggregation and uncertainty

- Report counts, percentages, averages, P95, min/max, and failures per category/tag.
- Repeat classification trials (proposed 3+) and report variance/confidence intervals.
- Use Wilson or bootstrap intervals for proportions; document method.
- Show per-case failures with redacted trace IDs; averages alone are insufficient.
- Compare cloud and local candidates side by side; do not aggregate across providers into one score.

## Baseline facts (not model results)

| Metric | Current |
| --- | --- |
| M-13 | 57 tests pass when two broken modules excluded; full collection fails |
| M-14 | 8 Ruff errors |
| M-15 | Discovery/architecture/implementation/security/deployment/operations/docs packs created; design partial |

## Gate use

| Gate | Metrics |
| --- | --- |
| G3 | M-01–M-10 for cloud and local candidates + approved cost model |
| G4 | M-11/M-12 + redaction/injection/approval tests |
| G5 | M-01–M-12 on holdout, plus M-13–M-15 current |

A threshold cannot be lowered in a results report. Change `../01-discovery/success-metrics.md` with
owner, date, and rationale.

## Traceability

Implements `BR-09`, `FR-13`, ADR-002/ADR-003, and `../08-operations/metrics.md`.
