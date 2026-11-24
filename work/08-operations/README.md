# Operations — `ai-agent-py`

Status: Operational specification · 2026-11-24

This pack defines observability, health, cost control, alerting, and incident handling for the
modular monolith. It is design guidance: the repository currently has stdout text only, with no
logging framework, metrics exporter, tracing, alert rules, budget controls, or incident process.

## Current operational state

| Area | Current |
| --- | --- |
| Logging | `print()` in `src/ai_agent/main.py` for response and token counts; `print()` in `__init__.py` |
| Levels/structure | None; no timestamps, environment, revision, trace IDs, or outcomes |
| Metrics | Provider token counts reach `ModelResponse` but are printed only by CLI |
| Tracing | None; no trace/span IDs or propagated context |
| Health | No service endpoint or probes; CLI exit only |
| Monitoring | Manual observation of stdout; no dashboards |
| Alerting | None |
| Cost | No price configuration, budget, attribution, or anomaly detection |
| Incidents | No severity, roles, runbooks, or postmortem process |

## Documents

| File | Purpose |
| --- | --- |
| `logging.md` | Structured event catalog, levels, fields, redaction, retention |
| `metrics.md` | Operational metric contract mapped to M-01–M-15 |
| `tracing.md` | Trace context, spans, sensitive-data rules, sampling |
| `monitoring.md` | Health checks, dashboards, SLOs, dependency visibility |
| `alerting.md` | Severity, thresholds, routing, suppression, alert catalog |
| `cost-management.md` | Usage/cost model, budgets, attribution, optimization |
| `incident-response.md` | Lifecycle, roles, playbooks, evidence, postmortems |

## Principles

1. Every operational signal must be redacted first; secrets and raw customer content never leave
   the process (`../06-security/pii-protection.md`, `../06-security/secrets-management.md`).
2. Logs answer “what happened”, metrics answer “how much/how often”, traces answer “where/when”.
   Do not duplicate one in another.
3. Every release record must state code revision, provider, model, prompt/profile versions,
   context limits, retry policy, dataset version, and deployment target.
4. “Unmeasured” is never rendered as zero or passing; CI gates and evaluation reports carry that
   status explicitly (`../01-discovery/success-metrics.md`).
5. Alerts must link a runbook and an owner; dashboards must link alerts and incident response.
6. Cost, latency, quality, and safety are reported together; optimizing one in isolation is not a
   release decision.

## Conventions

| Convention | Value |
| --- | --- |
| Service name | `ai-agent-py` |
| Environments | `dev`, `ci`, `evaluation`, `staging`, `prod` |
| Correlation | `trace_id`, `span_id` on logs, metrics exemplars, traces, incidents |
| Event names | Lowercase dot-separated, e.g. `model.call.completed` |
| Metric names | Lowercase snake_case with unit suffix where useful |
| IDs | Use authenticated tenant/principal IDs or hashes; never raw prompt/customer text as labels |
| Status | Current / Target / Proposed / Gap |

## Traceability

Supports `BR-09`, `BR-12`, `FR-15`, `NFR-08`, `NFR-11`, `NFR-12`, `NFR-13`, `SR-17`, gates G3–G5,
and `../07-deployment/infrastructure.md`.
