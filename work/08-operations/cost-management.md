# Cost Management

Status: Target cost model · No approved budget or price table exists today

## Current state

`OpenAIProvider` records input/output token counts in `ModelResponse`; `main.py` prints them for the
CLI demo. There is no price table, cost metric, budget, attribution, anomaly detection, retry cost
accounting, infrastructure allocation, or chargeback. The `README.md` figure of $44/day / $1,320 per
30 days is illustrative, not measured.

## Cost model

```text
ticket_cost =
  (input_tokens × input_price
   + output_tokens × output_price
   + cached_tokens × cached_price)
  × retry_multiplier
  + tool/infrastructure allocation
  + storage/observability allocation
```

All prices must come from a versioned, approved price table for the selected provider/model. Missing
prices produce `unmeasured` cost, not zero. Include retries explicitly: each attempt consumes tokens.
Include evaluation runs separately from production traffic.

## Cost dimensions

| Dimension | Allowed values / handling |
| --- | --- |
| Environment | `dev`, `ci`, `evaluation`, `staging`, `prod` |
| Provider / model | Registered IDs only |
| Generation profile | Registered task profile |
| Channel / route | Approved enum; no free text |
| Ticket category | Approved enum |
| Revision | Commit SHA |
| Tenant | Hashed/approved identifier only |
| Trace | `trace_id` for allocation and incident review |
| Attempt | Retry attempt number |

Never attach raw ticket text, prompts, outputs, tool payloads, or customer identifiers to cost
records.

## Metrics and reports

| Report | Source | Cadence | Audience |
| --- | --- | --- | --- |
| Live burn | `estimated_cost_minor_units`, `model_tokens_total` | Hourly/daily | On-call, product |
| Monthly M-09 | Usage × approved prices + infra allocation | Monthly | Product/finance |
| Per-provider comparison | Evaluation usage + infra cost | Per evaluation run | Engineering/product |
| Per-tenant showback | Hashed tenant + usage | Agreed cadence | Account owners |
| Release comparison | Revision, profile, prompt/model versions | Per release | Product/engineering |

Every report states dataset version where applicable, prompt version, model ID, provider, generation
profile, tool versions, context limits, retry policy, date, code revision, price-table version, and
currency. Missing fields mean the report is an estimate, not a result.

## Budgets (proposed, unmeasured)

| Scope | Budget | Alert | Action |
| --- | --- | --- | --- |
| Environment | Approved monthly amount per env | `COST-ANOMALY` | Notify owner; review mix |
| Provider/model | Approved per-model allocation | Model-specific anomaly | Switch only via approved policy |
| Tenant | Approved hashed-tenant quota | Quota warning/block | Throttle/limit with product approval |
| Evaluation | Approved per-run cap | Run-level stop | Abort and record partial results |
| Production per ticket | Approved ceiling by category/profile | Outlier alert | Review context/retry/prompt |

Absolute values require sponsor/finance approval. Do not derive production limits from the
illustrative README figure.

## Optimization levers

| Lever | Effect | Guardrail |
| --- | --- | --- |
| Context budgeting | Fewer input tokens | Do not drop authoritative system/tool facts; verify M-03 |
| Generation profiles | Smaller `max_output_tokens` per task | Verify M-02/M-03; no truncated answers |
| Prompt versioning/caching | Fewer repeated input tokens | Do not cache user-specific sensitive content without approval |
| Model selection | Lower unit price | Compare M-01–M-07; no silent fallback |
| Short-circuit classification | Avoid unnecessary generation | Verify M-01/M-04 |
| Retry/backoff tuning | Fewer duplicate calls | Keep bounded retries; no lost errors |
| Local Ollama | No per-call provider fee; infra/RAM/VRAM cost instead | Measure quality, latency, tool support; restricted network |
| Tool result shaping | Smaller untrusted payloads | Preserve required facts; treat as data |

## Controls

- Price table versioned with effective dates and currency.
- Cost emission uses only approved enums/hashes.
- Missing/unknown price blocks promotion of cost claims, not ticket handling.
- Cost exporter failure never breaks a response.
- Daily reconciliation between provider billing export and recorded token usage where available.
- Monthly reconciliation includes infrastructure, storage, logging, tracing, and evaluation costs.
- Budget exceptions require owner, expiry, and mitigation in the release record.
- Provider/model changes require updated price table and evaluation evidence before rollout.

## Verification

- Token totals from provider usage reconcile with metrics for a fixed fixture set.
- Retry attempts are charged; no attempt counted as free.
- Cached tokens counted only when provider reports them.
- Unknown model/price emits `unmeasured`, never zero.
- No secret/PII appears in cost dimensions, logs, or reports.
- Budget alert tests fire with synthetic usage below/above approved limits.
- Optimization changes compared on quality/latency metrics, not cost alone.

## Traceability

Supports M-08, M-09, `BR-09`, `FR-15`, `NFR-12`, `../08-operations/monitoring.md`, and
`../08-operations/alerting.md`.
