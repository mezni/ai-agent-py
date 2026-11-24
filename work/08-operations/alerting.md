# Alerting

Status: Target alert policy · No alert rules exist today

## Current state

There is no alerting system, severity model, routing, on-call schedule, runbook, suppression rule,
or escalation path. Failures are visible only if a human reads CLI stdout or a CI job fails.

## Severity model

| Severity | Meaning | Examples | Response |
| --- | --- | --- | --- |
| P1 / Critical | Active security/data-integrity incident or complete outage | Secret exposure, cross-owner access, unapproved consequential action, data corruption, total provider outage with no approved fallback | Immediate page; incident opened |
| P2 / High | Major degradation or likely incident | SLO/error-budget burn, migration failure, backup failure, high terminal failure rate, cost anomaly | Page on-call within agreed window |
| P3 / Medium | Localized degradation or trend | Retry spike, tool validation failures, single provider latency increase, dashboard gap | Ticket during business hours |
| P4 / Low | Informational/maintenance | Deploy notice, evaluation report available, expiring waiver | Notification only |

Severity must be approved by the incident owner; the table is a starting point.

## Alert anatomy

Every alert includes:

- stable `alert_id` and severity;
- environment, service, revision, provider/model where applicable;
- concise summary without sensitive content;
- metric/condition and observed vs. expected value;
- `runbook_id` link to `incident-response.md`;
- representative redacted `trace_id`/log examples;
- owner/routing target and escalation policy;
- suppression/maintenance state and start time.

Never include ticket text, prompts, model outputs, tool results, secrets, raw customer IDs, or raw
error bodies in alert payloads.

## Alert catalog

| Alert ID | Condition | Severity | Source | First action |
| --- | --- | --- | --- | --- |
| `SEC-SECRET-EXPOSURE` | Secret-like value in logs/artifacts/diff | P1 | Secret scan / log detector | Revoke/rotate; open incident |
| `SEC-OWNER-VIOLATION` | `owner_isolation_violations_total > 0` | P1 | Security metric/test | Disable path; preserve evidence |
| `SEC-UNAPPROVED-ACTION` | `approval_decisions_total{decision=missing} > 0` for consequential action | P1 | Approval gate | Block action; incident |
| `SEC-INJECTION-SIGNAL` | Injection test/control failure in production-like path | P1/P2 | Safety control | Deny untrusted content; investigate |
| `DATA-CORRUPTION` | Integrity/foreign-key check fails or unexpected row loss | P1 | Data health job | Stop writes; rollback plan |
| `MIGRATION-FAILED` | Migration exit non-zero or unknown/ahead schema at startup | P2 | Migration runner | Halt deploy; preserve backup |
| `BACKUP-STALE` | Last successful backup older than approved window | P2 | Backup job | Pause migration/release |
| `PROVIDER-DOWN` | Terminal provider errors exceed agreed error budget | P2 | `provider_errors_total` | Retry policy check; status review |
| `PROVIDER-LATENCY` | M-05/M-06 exceeds approved SLO for agreed window | P2/P3 | Latency histograms | Check provider/profile/context |
| `TOOL-FAILURE-SPIKE` | Tool validation/outcome failures above agreed rate | P3 | `tool_calls_total` | Inspect tool schema/data path |
| `RETRY-STORM` | `retry_attempts_total` above agreed rate | P3 | Retry telemetry | Check provider/config/backoff |
| `COST-ANOMALY` | Daily/monthly burn above approved budget or unexpected model/profile mix | P2/P3 | Cost metrics | Pause expensive path; review |
| `EVAL-REGRESSION` | Holdout M-01–M-12 below gate or baseline regression | P2/P3 | Evaluation report | Block promotion; compare revision |
| `CI-GATE-FAILED` | M-13/M-14/gate failure on release branch | P3 | CI | Fix before promotion |
| `MONITORING-GAP` | Required metric/log/trace absent beyond approved window | P3 | Self-check | Restore instrumentation/data |

Thresholds are intentionally expressed as “agreed”/“approved”; no absolute production threshold has
been measured or accepted yet. Define them with SLOs in `monitoring.md` and budgets in
`cost-management.md`.

## Routing and escalation

| Environment | Routing | Notes |
| --- | --- | --- |
| `dev` / `ci` | Developer/CI channel | No paging |
| `evaluation` | Evaluation owner | Quality/cost findings |
| `staging` | Engineering on-call | Rehearsal alerts expected during drills |
| `prod` | Role-based on-call + security for P1 | Named rotation not defined; owner approval required |

Escalation sequence: acknowledge → triage → contain → assign incident commander if P1/P2 → notify
owner → unresolved escalation after agreed interval. Document names/rotations outside Git.

## Suppression and fatigue control

- Suppress duplicate alerts for the same condition/revision/environment; group by root cause.
- Maintenance windows require owner, reason, start/end, and affected alert IDs.
- Flapping requires a for-duration and recovery condition; never alert on a single sample unless
  security/data-critical.
- Re-evaluate every rule after an incident; delete rules that never lead to action.
- Alert on absence of expected signals (dead-man's switch) for critical pipelines/backups.
- Never suppress P1 secret/owner/approval/corruption conditions without security approval.

## Verification

- Every alert condition has a test fixture with a firing and non-firing case.
- Every alert payload passes the sensitive-data allowlist test.
- Every alert links a valid runbook and owner/role.
- P1 alerts open an incident automatically or via documented manual step.
- Maintenance/suppression rules expire and are logged.
- Alert thresholds link to approved SLO/budget IDs; unmeasured thresholds are not enabled.

## Traceability

Implements M-09–M-14, `NFR-08`, `NFR-11`, `NFR-12`, `SR-19`, and
`../08-operations/incident-response.md`.
