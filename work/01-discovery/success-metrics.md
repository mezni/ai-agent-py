# Success Metrics

Status: Proposed targets · No measured product or model results yet · 2026-11-24

## North star

The project succeeds when it can repeatedly resolve representative support tickets with correct,
grounded, approved answers inside agreed latency, cost, and safety limits — with evidence that
anyone can reproduce.

## Metric definitions

| ID | Metric | Baseline | Proposed target | Measurement method | Instrumentation needed |
| --- | --- | --- | --- | --- | --- |
| M-01 | Classification accuracy | Unmeasured | ≥95% | Labeled representative dataset; exact category match | Evaluation results per ticket |
| M-02 | Structured-output validity | Unmeasured | ≥99% | Complete response parses and passes schema/business validation | Parser/validator outcomes |
| M-03 | Response correctness / groundedness | Unmeasured | Agree threshold with owner | Human rubric plus tool-fact attribution | Review labels and trace IDs |
| M-04 | Tool-call success rate | Unmeasured | Agree threshold with owner | Correct tool, valid args, expected result on scenario set | Tool name, args hash, outcome |
| M-05 | Average end-to-end latency | Unmeasured | <2 s | Time from request receipt to complete response | Timestamps per request |
| M-06 | P95 end-to-end latency | Unmeasured | Agree threshold with owner | Same dataset under agreed load | Latency histogram |
| M-07 | TTFT | Unmeasured | Agree threshold with owner | First streamed chunk timestamp | Stream events |
| M-08 | Token usage per ticket | Printed for CLI demo only | Within cost model | Input/output/cached tokens from provider | Provider usage records |
| M-09 | Cost per ticket / month | Illustrative $44/day, $1,320/30 days | Within approved budget | Usage × prices + retries + infrastructure | Usage and infra reports |
| M-10 | Retry and failure rate | Unmeasured | Within agreed error budget | Error class, retry count, terminal failure | Structured error logs |
| M-11 | Owner-isolation violations | No auth layer; unmeasured | 0 | Cross-owner access tests and audit review | Owner ID + access logs |
| M-12 | Unapproved consequential actions | Approval not implemented | 0 | Approval-flow test and audit records | Approval decisions |
| M-13 | Test pass rate | 57 pass; 2 collection errors | 100% of selected suite passing | `uv run pytest -q` | CI results |
| M-14 | Lint findings | 8 Ruff errors | 0 | `uv run ruff check .` | CI results |
| M-15 | Documentation/decision coverage | README, LOG, SUMMARY exist; specs new | All significant decisions have ADRs | Review checklist | ADR index |

## Baseline

The only objective results available at discovery time are engineering checks: 57 tests pass when
the two broken modules are excluded; full collection fails on `Iterator` and `LLMValidationError`;
Ruff reports 8 errors. Model quality, latency, cost, and groundedness have not been measured.
The 95%, 99%, and <2 s figures in `README.md:208-210` are proposed targets, not achieved results.

## Evaluation design

### Dataset

- Use a versioned, representative ticket set agreed with the sponsor and data owner.
- Include each supported category, ambiguous tickets, tool-dependent order/customer questions,
  FAQ questions, malformed or incomplete requests, and prompt-injection attempts in tool output.
- Record language, category, expected tool calls, expected answer facts, and human-review labels.
- Keep an immutable holdout set for final acceptance; tune prompts/profiles on a separate split.

### Procedure

1. Freeze prompt version, model ID, generation profile, tool schemas, and context settings.
2. Run each candidate provider/profile on the same dataset with the same retry policy.
3. Measure M-01–M-10 per ticket; store raw outputs, traces, and derived metrics.
4. Repeat classification trials to quantify variance, especially at `temperature=0.0`.
5. Compare cloud and local providers on quality, average/P95 latency, token usage, infrastructure
   cost, RAM/VRAM, and tool-calling support.
6. Report confidence intervals and failure examples, not only averages.

### Safety evaluation

- Verify no cross-owner reads, writes, or deletes (M-11).
- Verify no consequential action executes without an approval record (M-12).
- Verify tool results, memory, and summaries cannot override system instructions.
- Verify partial streamed JSON is never accepted as a classification result.
- Verify secrets and sensitive content do not appear in logs or traces.

## Exit gates

| Gate | Exit criteria |
| --- | --- |
| G1 — Discovery | Sponsor confirms scope, users, volume, budget, providers, and approval roles; `Q-01`–`Q-12` resolved or explicitly waived |
| G2 — Foundation | Canonical model contract chosen; config package importable; full tests and lint pass; baseline report recorded |
| G3 — Evaluation | Dataset frozen; harness reports M-01–M-10 for at least one cloud and one local candidate; cost model approved |
| G4 — Safety | Owner isolation, approval gate, untrusted-data handling, and log redaction tests pass; security/provider approval recorded |
| G5 — Acceptance | End-to-end flow meets agreed M-01–M-12 thresholds on holdout data; documentation and ADRs current |

## Reporting rule

Every metric report must state the dataset version, prompt version, model ID, provider,
generation profile, tool versions, context limits, retry policy, date, and code revision. A metric
without those fields is an estimate, not a result.
