# Evaluation Results

Status: Template · No evaluation run has been performed · 2026-11-24

## Current status

No harness exists and no provider/model comparison has been run. All model quality, latency,
groundedness, tool, cost, retry/failure, owner-isolation, and approval metrics are **unmeasured**.
This file is the required evidence artifact for gates G3/G5, not evidence that the gates passed.

## Dataset

| Field | Value |
| --- | --- |
| Dataset | `evaluation-dataset.jsonl` |
| Version | `2026-11-24-v1` (seed; owner freeze pending) |
| SHA-256 | `5577756f5d49496d3640d96297d499b170f73967cfb0606950729108f8c839f9` |
| Cases | 30 |
| Splits | dev / holdout |
| Source | Synthetic, sanitized |
| Freeze owner | Pending product/data owner approval |

## Run metadata template

| Field | Value |
| --- | --- |
| Run ID |  |
| Date / operator |  |
| Harness version / code revision |  |
| Dataset version / SHA-256 / split |  |
| Provider / model / model version |  |
| Prompt name:version / schema version |  |
| Generation profile / settings / token caps |  |
| Context limits / response reserve |  |
| Retry policy / timeout / fault injection |  |
| Tool versions |  |
| Price table version / currency |  |
| Repetitions / confidence method |  |
| Evidence links (logs/traces/report) |  |

## Results

| ID | Metric | Target | Result | Confidence / failures | Status |
| --- | --- | --- | --- | --- | --- |
| M-01 | Classification accuracy | ≥95% proposed | Unmeasured | — | Not run |
| M-02 | Structured-output validity | ≥99% proposed | Unmeasured | — | Not run |
| M-03 | Correctness / groundedness | Owner threshold pending | Unmeasured | — | Not run |
| M-04 | Tool-call success rate | Owner threshold pending | Unmeasured | — | Not run |
| M-05 | Average latency | <2 s proposed | Unmeasured | — | Not run |
| M-06 | P95 latency | Owner threshold pending | Unmeasured | — | Not run |
| M-07 | TTFT | Owner threshold pending | Unmeasured | — | Not run |
| M-08 | Token usage per ticket | Within cost model | Unmeasured | CLI prints demo counts only | Not run |
| M-09 | Cost per ticket / month | Approved budget pending | Unmeasured | README example illustrative | Not run |
| M-10 | Retry / failure rate | Agreed error budget pending | Unmeasured | Fault cases defined | Not run |
| M-11 | Owner-isolation violations | 0 | Unmeasured | No auth layer; tests absent | Blocked |
| M-12 | Unapproved consequential actions | 0 | Unmeasured | No approval gate | Blocked |
| M-13 | Test pass rate | 100% | Baseline only: 57 pass with 2 modules excluded; full collection fails | `Iterator`, `LLMValidationError` | Not passed |
| M-14 | Lint findings | 0 | 8 errors | Ruff baseline | Not passed |
| M-15 | Documentation/decision coverage | All significant decisions | Partial | Specs created; design/eval gaps | In progress |

## Candidate comparison

| Candidate | Provider/model | Profile/prompt | M-01 | M-02 | M-05/M-06 | M-08/M-09 | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | TBD approved OpenAI ID | classification / `1.0.0` | Unmeasured | Unmeasured | Unmeasured | Unmeasured | Not run |
| C2 | TBD approved OpenAI ID | alternative / `2.0.0` | Unmeasured | Unmeasured | Unmeasured | Unmeasured | Not run |
| C3 | TBD local Ollama ID | classification / `1.0.0` | Unmeasured | Unmeasured | Unmeasured | Unmeasured | Not run |

Placeholder model IDs and `context_window=0` from the model catalog are not valid candidates.

## Per-category report template

| Category | Cases | Correct | Accuracy | Valid outputs | Tool success | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| order_status | — | — | Unmeasured | Unmeasured | Unmeasured | Fill after run |
| refund | — | — | Unmeasured | Unmeasured | Unmeasured | Fill after run |
| technical_support | — | — | Unmeasured | Unmeasured | Unmeasured | Fill after run |
| account | — | — | Unmeasured | Unmeasured | Unmeasured | Fill after run |
| general | — | — | Unmeasured | Unmeasured | Unmeasured | Fill after run |

## Safety results

| Area | Cases | Result | Evidence |
| --- | --- | --- | --- |
| Tool-output injection | EV-021 | Unmeasured | No harness |
| Memory injection | EV-022 | Unmeasured | No harness |
| Ticket-text injection | EV-023 | Unmeasured | No harness |
| Secret extraction | EV-024 | Unmeasured | No harness |
| PII redaction | EV-030 | Unmeasured | No harness |
| Owner isolation | `regression-tests.md` | Unmeasured | No auth layer |
| Approval gate | `regression-tests.md` | Unmeasured | Not implemented |
| Partial/invalid output | `regression-tests.md` | Unmeasured | Validation import broken |

## Failure examples

No evaluated failures exist because no run occurred. After a run, list case IDs, redacted trace IDs,
expected vs actual, error class, and mitigation. Do not paste raw tickets, prompts, model outputs,
tool payloads, or secrets.

## Gate decision

| Gate | Status | Reason |
| --- | --- | --- |
| G3 — Evaluation | Blocked | Dataset seed exists but no owner freeze, harness, M-01–M-10 results, or approved cost model |
| G4 — Safety | Blocked | Owner isolation, approval, redaction, and untrusted-data tests not implemented |
| G5 — Acceptance | Blocked | No holdout results and code quality gates failing |

## Sign-off

| Role | Name | Decision | Date | Evidence |
| --- | --- | --- | --- | --- |
| Product/data owner |  | Freeze / reject dataset |  |  |
| Evaluation owner |  | Accept run |  |  |
| Security owner |  | Accept safety results |  |  |
| Engineering owner |  | Accept gate decision |  |  |

## Traceability

Required artifact for G3/G5 in `../04-implementation/quality-gates.md`; definitions in `metrics.md`;
method in `evaluation-strategy.md`.
