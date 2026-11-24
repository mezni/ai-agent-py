# Operations

Status: Operational summary · No implementation exists today · 2026-11-24

## Current state

| Area | Current |
| --- | --- |
| Logging | `print()` only in `main.py`/`__init__.py`; no levels, trace IDs, or redaction |
| Metrics | Token counts printed, not exported |
| Tracing | None |
| Health/monitoring | No endpoint, dashboard, SLO, or dependency check |
| Alerting | None |
| Cost | No price table, budget, attribution, or anomaly detection |
| Incidents | No severity, roles, runbooks, or postmortems |

The full target design is in `../08-operations/`.

## Signal contract

| Signal | Purpose | Rules |
| --- | --- | --- |
| Logs | Structured events: what happened | JSON fields, levels, stable event names, redaction |
| Metrics | How often/how much | Counters/histograms/gauges; approved low-cardinality labels |
| Traces | Where/when in the request | `trace_id`/`span_id` across model/tool/store/approval |
| Alerts | Actionable degradation | Owner, runbook, redacted evidence, severity |
| Cost | Token/infra spend | Versioned prices, no raw customer data |

Never log/export secrets, raw prompts, model outputs, tool payloads, PII, or raw owner IDs. Missing
data is reported as `unmeasured`, never zero or passing.

## Health and SLOs

A health endpoint is added only with a transport adapter. Until then, startup validation, migration
status, CLI smoke tests, and CI gates are the health checks. Proposed SLOs (availability, M-05/M-06
latency, M-01–M-04 quality, M-10 failures, M-11/M-12 safety, M-09 cost) require owner approval
before becoming alerts.

## Dashboards

Service overview, LLM quality, latency/streaming, tools/data, safety/security, cost, reliability,
delivery, and data health. Every panel links its metric definition, runbook, and alert; annotations
mark releases, provider/model changes, and migrations. See `../08-operations/monitoring.md`.

## Alerting

| Severity | Examples | Response |
| --- | --- | --- |
| P1 | Secret exposure, owner breach, unapproved action, data corruption | Immediate page + incident |
| P2 | SLO burn, migration/backup failure, cost anomaly | On-call |
| P3 | Retry spike, tool validation spike, model regression | Ticket |
| P4 | Informational | Notification |

Alert payloads carry `alert_id`, severity, environment, revision, redacted evidence, and a runbook
link. Thresholds are not enabled until tied to approved SLOs/budgets. See
`../08-operations/alerting.md`.

## Cost control

Cost = provider token usage × versioned prices, including retries, plus infrastructure/storage/
observability allocation. Reports must state code revision, provider, model, prompt/profile,
context limits, retry policy, price-table version, and currency. Budgets require approval; the
README's $44/day example is illustrative, not measured. See
`../08-operations/cost-management.md`.

## Troubleshooting quick map

| Symptom | First check | Then |
| --- | --- | --- |
| `KeyError` on startup | `.env` / environment | Restore variables; deployment should fail clearly |
| Full pytest collection error | `Iterator`, `LLMValidationError` | Fix per `DEVELOPMENT.md` |
| Slow responses | M-05/M-06, context size, retries, provider latency | Tune context/profile; check provider |
| Tool failures | Allowlist, strict args, tool outcome metrics | Validate schema/handler; deny unknown tools |
| Cost spike | Model mix, retries, cached tokens, budget | Pause path; review profile/model |
| Cross-owner/approval concern | M-11/M-12 and audit logs | Treat as P1; follow `RUNBOOK.md` |
| Migration failure | `schema_migrations`, backup, integrity checks | Stop writes; rollback plan |

## Incident link

P1/P2 conditions follow `../08-operations/incident-response.md`; immediate steps are in
`RUNBOOK.md`.

## Traceability

Summarizes `../08-operations/README.md`, `logging.md`, `metrics.md`, `tracing.md`, `monitoring.md`,
`alerting.md`, `cost-management.md`, and `incident-response.md`.
