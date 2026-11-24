# Evaluation Strategy

Status: Proposed harness and procedure · 2026-11-24

## Goals

- Measure M-01–M-12 on a frozen, representative, sanitized ticket set.
- Compare approved cloud and local candidates on the same cases and settings.
- Prove safety rules (owner isolation, approval, injection, redaction) with deterministic cases.
- Produce evidence that another team can replay from a clean checkout.

## Principles

1. Freeze dataset, prompt, schema, provider, model, profile, context limits, retry policy, tool
   versions, code revision, and price table before a run.
2. Dev split is for tuning; holdout split is for acceptance and is not inspected during tuning.
3. Report failures, confidence intervals, and trace IDs, not only averages.
4. A classification category never authorizes an action or business fact.
5. Untrusted tool/memory output is data, never instructions.
6. Unmeasured results do not pass G3/G5.

## Dataset design

`evaluation-dataset.jsonl` is a seed dataset requiring owner freeze. It includes:

- all five supported categories;
- order IDs `4821`, `4822`, `4823` from mock authoritative data;
- ambiguous, malformed, empty, non-English, typo, and long-context cases;
- prompt-injection attempts via tool output, memory, and ticket text;
- PII-redaction expectations;
- retry/failure-injection cases;
- dev and holdout splits.

Distribution and representativeness must be confirmed with the sponsor/data owner (`Q-01`); the
seed set is not evidence of production distribution.

## Harness contract

The harness must accept:

```text
--dataset <path> --dataset-version <id> --split dev|holdout|all
--provider <openai|ollama> --model <id> --profile <name>
--prompt <name:version> --schema-version <id>
--context-limits <max,reserve> --retry-policy <id>
--repetitions <n> --output <report path>
```

It must record for each case:

- case ID, split, tags, prompt/model/profile/schema versions;
- raw provider status/finish reason and normalized output, with sensitive content redacted;
- parsed `TicketClassification`, validation outcome, and error class;
- chosen tool calls, argument validity, authoritative facts used;
- trace ID, latency, TTFT, token usage, retry attempts, estimated cost;
- expected vs. actual category, validity, groundedness/tool outcome, and safety flags.

Live provider calls are allowed only in the evaluation job with controlled credentials. Unit tests
must use fakes.

## Procedure

1. Resolve blockers that prevent clean execution (`Iterator`, `LLMValidationError`, config
   shadowing, canonical contract, `ollama` dependency, classifier SDK/env coupling).
2. Freeze dataset and record its SHA-256.
3. Run dev split for each candidate provider/profile with fixed settings.
4. Tune prompts/profiles only on dev; record every change.
5. Re-freeze final settings; run holdout once for acceptance candidates.
6. Repeat classification trials (proposed 3+) to quantify variance, especially with low temperature.
7. Compute M-01–M-12 per case, then aggregate with confidence intervals.
8. Run safety regression suite (`regression-tests.md`) with fault injection.
9. Write `evaluation-results.md` with evidence links and gate decision.
10. Preserve report, logs, traces, and failed examples with redaction.

## Candidate matrix

| Candidate | Provider | Model | Profile | Prompt | Required evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | OpenAI | approved ID | classification low-variation | `ticket_classification:1.0.0` | M-01–M-12, cost, latency |
| C2 | OpenAI | approved ID | alternative token cap | `ticket_classification:2.0.0` | M-01–M-12, cost, latency |
| C3 | Ollama | approved local ID | classification low-variation | same prompt | M-01–M-12, infra cost, RAM/VRAM, tool support |
| Fallback | TBD | TBD | TBD | TBD | Only after ADR-005 approval |

Do not use placeholder model IDs or `context_window=0`. Verify capability flags with the provider.

## Safety evaluation

- Injection cases: tool output, memory, and ticket text must not override instructions.
- PII cases: sensitive values must be absent from logs/traces and answers must not reveal secrets.
- Owner isolation: no cross-owner read/write/delete (`M-11`).
- Approval: no consequential action without recorded approval (`M-12`).
- Structured output: partial streamed JSON, refusals, incomplete responses, extra fields, invalid
  categories, and missing order IDs must fail explicitly.
- Tool use: unknown tools and invalid arguments must be denied before handlers execute.

## Metrics and thresholds

See `metrics.md` for formulas. Proposed targets:

| Metric | Target | Status |
| --- | --- | --- |
| M-01 | ≥95% | Proposed, unmeasured |
| M-02 | ≥99% | Proposed, unmeasured |
| M-05 | <2 s avg | Proposed, unmeasured |
| M-11 / M-12 | 0 | Required, untested |
| M-13 / M-14 | 100% / 0 | Current baseline failing |

Threshold changes must be made in `../01-discovery/success-metrics.md` with owner/date/rationale.

## Gate decisions

| Gate | Requires |
| --- | --- |
| G3 | Frozen dataset/harness; M-01–M-10 for cloud and local candidates; approved cost model |
| G5 | M-01–M-12 on holdout meets agreed thresholds; docs/ADRs current; sign-off |

## Evidence and privacy

- Store only redacted raw outputs and traces needed to review failures.
- Do not attach real customer data, secrets, or production keys to reports.
- Link code revision, dataset hash, provider/model/profile/prompt/schema versions, price table,
  retry policy, context limits, date, and operator.
- Preserve failed example IDs; do not hide failures behind averages.

## Traceability

Implements `BR-09`, `FR-13`, `NFR-01`, `NFR-04`, ADR-002, ADR-003, gates G3/G5, and
`../04-implementation/testing-strategy.md`.
