# Evaluation — `ai-agent-py`

Status: Evaluation specification and seed dataset · 2026-11-24

Goal: make quality, latency, cost, and safety claims reproducible before release. This pack defines
the dataset, harness contract, metrics, results template, and regression cases. It does **not**
claim measured results: no harness has been run and no thresholds have been accepted.

## Current state

| Item | Status |
| --- | --- |
| Dataset | Seed JSONL in `evaluation-dataset.jsonl`; requires data owner freeze/sign-off |
| Harness | Not implemented |
| Results | Unmeasured; see `evaluation-results.md` |
| CI gate | G3/G5 blocked (`../04-implementation/quality-gates.md`) |
| Baseline | 57 tests pass when broken modules excluded; full collection fails; 8 Ruff errors |
| Model/provider comparison | Not performed |
| Cost model | Illustrative only in root README |

## Documents

| File | Purpose |
| --- | --- |
| `README.md` | Index, dataset schema, status, and usage rules |
| `evaluation-strategy.md` | Dataset design, harness, procedure, providers, safety, gates |
| `evaluation-dataset.jsonl` | Versioned synthetic ticket cases with expected outcomes |
| `metrics.md` | M-01–M-15 definitions, formulas, instrumentation, reporting rules |
| `evaluation-results.md` | Run metadata and results template; currently unmeasured |
| `regression-tests.md` | Deterministic regression/security cases linked to dataset IDs |

## Dataset schema

Each JSONL line is one case:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable case ID (`EV-001`) |
| `dataset_version` | string | Freeze identifier |
| `split` | `dev` / `holdout` | Dev for tuning; holdout for acceptance only |
| `language` | string | Ticket language/code |
| `ticket` | string | Synthetic sanitized ticket text |
| `expected_classification` | object / null | `category`, `order_id`, `needs_order_lookup` |
| `expected_tool_calls` | array | Authoritative tool calls expected downstream |
| `expected_answer_facts` | array | Facts the final answer must contain or constraints it must honor |
| `tags` | array | Categories such as `order`, `injection`, `retry`, `pii` |
| `notes` | string | Interpretation guidance |
| `expected_error` | string / absent | Expected controlled failure when no result is valid |
| `untrusted_tool_output` | string / absent | Injected tool/memory text for safety cases |
| `simulate_provider_error` | string / absent | Harness fault injection instruction |

## Dataset rules

1. Synthetic and sanitized only; no customer tickets, real IDs, keys, or PII.
2. Categories must match the strict schema: `order_status`, `refund`, `technical_support`,
   `account`, `general` (`src/ai_agent/domain/ticket_classification.py`).
3. `needs_order_lookup=true` requires a non-null `order_id` and `category=order_status`
   (`ticket_validation.py`).
4. Mock authoritative facts come only from `order_tools.py`, `customer_tools.py`, and
   `knowledge_tools.py`.
5. Holdout cases are never used for prompt/profile tuning; inspect them only during acceptance.
6. Change the dataset version and record owner/reason when any case changes.

## Freeze checklist

- [ ] Product/data owner approves category distribution and expected labels.
- [ ] Security owner approves injection/PII cases.
- [ ] Dataset hash recorded in `evaluation-results.md`.
- [ ] Split and holdout access rules accepted.
- [ ] Harness can replay the exact version from a clean checkout.

## Source-of-truth rules

- Requirements/targets: `../01-discovery/success-metrics.md`.
- Decision context: `../02-architecture/adr/ADR-002-llm-classification.md` and `ADR-003`.
- Test strategy: `../04-implementation/testing-strategy.md`.
- Gate semantics: `../04-implementation/quality-gates.md`.
- “Unmeasured” never means zero, passing, or not applicable.

## Traceability

Supports `BR-09`, `FR-13`, gates G3/G5, and M-01–M-15.
