# Monitoring

Status: Target monitoring design · No dashboards or health checks exist today

## Current state

Monitoring is manual stdout inspection. The CLI prints a response and token counts, then exits. There
is no liveness/readiness endpoint, dashboard, service-level objective, dependency check, retention
view, or alert linkage. Missing configuration fails during import with `KeyError`.

## Health model

A health endpoint is added only when a transport adapter exists. Until then, startup validation,
migration status, CLI smoke tests, and CI gates are the health checks.

| Check | Type | Pass condition | Failure action |
| --- | --- | --- | --- |
| Liveness | Runtime | Process responsive; no deadlock in request loop | Restart process |
| Readiness | Traffic | Config valid, schema version current, DB writable, required provider capability verified | Remove from traffic; no ticket processing |
| Startup | Deployment | Settings validated, secrets present but unlogged, migrations applied, model/provider explicit | Fail deployment |
| Dependency | Continuous | Provider reachable within timeout; optional Ollama reachable if enabled | Degrade/alert; no silent provider fallback |
| Data | Continuous | `PRAGMA integrity_check`, `foreign_key_check`, backup job succeeded | Page data owner; stop writes if corruption suspected |
| Security | Continuous | Owner scoping and approval gate enabled; no critical control disabled | Deny traffic; incident |

Readiness must not call a live provider on every probe. Use cached startup capability checks and a
bounded, sampled dependency check.

## Service-level objectives (proposed, unmeasured)

| SLO | Measure | Target | Owner approval |
| --- | --- | --- | --- |
| Availability | Successful requests / valid requests | Owner-defined; do not infer from CLI | Pending |
| Latency | M-05 average, M-06 P95 | README proposes <2 s average; threshold pending | Pending |
| Quality | M-01–M-04 | ≥95% classification and ≥99% structured validity proposed; others pending | Pending |
| Reliability | M-10 terminal failure rate | Within agreed error budget | Pending |
| Safety | M-11 = 0, M-12 = 0 | Zero tolerance | Pending |
| Cost | M-09 monthly | Within approved budget | Pending |

An SLO without an agreed measurement method is a proposal. Do not convert it into an alert threshold
without `alerting.md` approval.

## Dashboards

| Dashboard | Audience | Panels |
| --- | --- | --- |
| Service overview | On-call | availability, request rate, error rate, latency hist, recent deploys, active alerts |
| LLM quality | Product/eval | M-01–M-04 by category/model/profile, confidence distribution, failure samples via trace IDs |
| Latency and streaming | Engineering | M-05, M-06, M-07, TTFT, provider latency, queue/retry impact |
| Tools and data | Engineering | M-04 by tool, validation failures, store/memory outcomes, denials |
| Safety and security | Security | M-11, M-12, approval decisions, authorization denials, prompt-injection test rate |
| Cost | Product/finance | M-08, M-09, cost by environment/provider/model/profile, budget burn |
| Reliability | On-call | M-10, retry attempts, error class breakdown, provider/outage status |
| Delivery | Engineering | M-13, M-14, M-15, release/ADR coverage, migration status |
| Data health | Data owner | migration version, integrity/foreign-key checks, backup age/result |

## Panel rules

- Show `unmeasured` explicitly where no data exists; never show a green zero.
- Every panel links its metric definition, runbook, and relevant alert.
- Compare current release with previous release and evaluation baseline.
- Break down by approved labels only: environment, provider, model, profile, category, tool,
  outcome, error class, revision.
- Include trace IDs/examples in failure panels; no raw ticket/model content.
- Mark provider/model changes and migration windows as annotations.

## Dependency visibility

| Dependency | Signal | Degraded behavior |
| --- | --- | --- |
| OpenAI | error rate, latency, token usage, finish reason | Retry bounded; controlled error; no silent fallback |
| Ollama | reachability, latency, memory/VRAM if exposed by platform | Explicit disabled/degraded state; no automatic provider switch |
| SQLite | file writable, integrity check, migration version, lock/timeout errors | Readiness fail; no writes until resolved |
| Secret store | secret fetch success; no values displayed | Startup fail; deploy blocked |
| CI/evaluation | gate status, dataset version, report age | Promotion blocked |
| Backup job | last success age and restore test | Migration/release blocked |

## Correlation workflow

1. Alert or dashboard anomaly provides `alert_id`, `trace_id`, revision, and environment.
2. Logs show structured events for that trace with redacted fields.
3. Trace shows which span failed/slowed (model, tool, store, approval, context).
4. Cost dashboard shows whether retries/provider/model/profile changed.
5. Incident record links all evidence and the release record.

## Verification

- Startup fails clearly with missing/invalid configuration.
- Readiness fails with unknown/ahead schema version, unwritable DB, or invalid provider capability.
- Every dashboard metric exists for at least one fixture run.
- Unmeasured values render as `unmeasured`.
- Annotations appear for releases, provider/model changes, and migrations.
- Dashboard queries reject forbidden labels and raw text.
- Alert links resolve to `alerting.md` and `incident-response.md`.

## Traceability

Implements M-01–M-15, `NFR-08`, `NFR-12`, `SR-19`, and
`../07-deployment/infrastructure.md`.
