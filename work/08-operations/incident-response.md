# Incident Response

Status: Target process · No incident process exists today

## Current state

There is no defined severity, role, on-call rotation, runbook, evidence-preservation rule,
postmortem template, or drill. Today a failure is noticed by a developer reading stdout or CI output.
No automated link exists between alerts, logs, traces, release records, and rollback.

## Severity and scope

| Severity | Definition | Examples | Commander |
| --- | --- | --- | --- |
| P1 | Active security/data-integrity incident or full outage | Secret exposure, owner-isolation breach, unapproved consequential action, data corruption, provider outage with no approved path | Assigned immediately |
| P2 | Major degradation or credible incident | SLO burn, cost anomaly, migration failure, backup failure | Assigned promptly |
| P3 | Localized degradation | Retry spike, tool validation failures, single-model regression | Owner ticket |
| P4 | Informational | Deploy notice, report available, waiver expiring | No incident required |

Severity can be raised by security/compliance at any time.

## Roles

| Role | Responsibility |
| --- | --- |
| Incident commander | Coordinates decisions, timeline, escalation, and closure |
| Operations/on-call | Containment, deployment/rollback, health verification |
| Engineering owner | Code/config/provider diagnosis and fix |
| Security/compliance owner | Secret, PII, authorization, approval, and provider-term decisions |
| Product/data owner | Customer impact, data recovery approval, communications |
| Communications owner | Internal/external updates; no raw sensitive details |

Named people/rotations are kept outside Git. One person may hold multiple roles, but P1 security
decisions require the security owner.

## Lifecycle

1. **Detect** — alert, test failure, user report, or manual observation; create incident ID.
2. **Triage** — assign severity/commander; record environment, revision, release, provider/model,
   prompt/profile, and first seen time.
3. **Contain** — stop new work/traffic, disable affected path, revoke secrets if exposed, preserve
   logs/traces/artifacts.
4. **Diagnose** — correlate alert → logs → trace → metrics → cost → release/migration record.
5. **Mitigate** — apply rollback (`../07-deployment/rollback-strategy.md`), config/provider/prompt
   restore, or forward fix under change control.
6. **Recover** — run readiness, smoke tests, owner-isolation test, migration status, and monitoring
   verification; watch an agreed observation window.
7. **Close** — record impact, root cause, actions, evidence, and follow-up owners/dates.
8. **Learn** — blameless postmortem for P1/P2; convert actions into issues, tests, alerts, or ADRs.

## Playbooks

| Incident | Immediate containment | Recovery check |
| --- | --- | --- |
| Secret exposure | Revoke/rotate; disable affected artifact/job; preserve evidence | Secret scan clean; new key injected; no secret in logs/artifacts |
| PII/memory leakage | Disable affected path; stop affected log export; assess scope | Redaction tests pass; retention/deletion decision applied |
| Owner-isolation breach | Deny affected route/tool; audit access records | Cross-owner tests pass; affected records reviewed |
| Unapproved consequential action | Block approval gate; stop tool class | Missing-approval count zero; audit complete |
| Prompt injection via tool/memory | Treat source as untrusted; disable affected tool/source | Injection regression tests pass; no instruction override |
| Provider outage | Stop retries storm; check status/budget; no silent fallback | Provider health restored or approved alternate path |
| Model/prompt quality regression | Pin previous model/prompt/profile; block promotion | Holdout M-01–M-04 compared and accepted |
| Cost spike | Pause expensive path/tenant; cap evaluation runs | Cost reconciled; budget restored; cause documented |
| Migration/data failure | Stop writes; use backup/down plan | `schema_migrations`, integrity/foreign-key checks, smoke tests pass |
| Monitoring/alert failure | Use manual watch; assume alerts blind | Synthetic alert test passes; dashboards populated |

## Evidence set

Record links/IDs only; never paste raw secrets, prompts, ticket text, model outputs, or tool payloads
into incident documents.

| Evidence | Source |
| --- | --- |
| Incident ID, timeline, decisions | Incident record |
| Alert ID and payload | `alerting.md` |
| Structured logs | `logging.md` |
| Trace IDs/spans | `tracing.md` |
| Metrics/dashboard snapshot | `metrics.md`, `monitoring.md` |
| Cost snapshot | `cost-management.md` |
| Release record, image digest, config version | `../07-deployment/ci-cd.md` |
| Migration version and backup result | `../07-deployment/database-migrations.md` |
| Rollback target and actions | `../07-deployment/rollback-strategy.md` |
| Evaluation report | `../01-discovery/success-metrics.md` |

## Communications

- First update: severity, affected environment/service, containment status, next update time.
- Later updates: impact, mitigation progress, decisions needing owner approval.
- Closure: customer-facing impact, recovery time, follow-ups, no sensitive details.
- Security/legal/compliance decides external disclosure; do not speculate in incident notes.

## Postmortem template

| Section | Content |
| --- | --- |
| Summary | What happened, impact, duration, severity |
| Timeline | Detection → triage → containment → recovery, UTC timestamps |
| Contributing factors | Code, config, provider, process, monitoring gaps |
| What went well / poorly | Evidence-based observations |
| Root cause | Verified cause; avoid blame |
| Detection gap | Which alert/log/trace/test was missing or noisy |
| Actions | Owner, due date, test/ADR/alert link |
| Decisions | Rollback, waiver, provider/terms, approvals |
| Evidence | IDs/links from the evidence set |

## Drills

- Restore backup and migrate rollback in staging.
- Revoke/rotate a fake secret and verify no exposure.
- Trigger a synthetic P1 owner-isolation alert end to end.
- Rehearse provider outage and cost-spike containment.
- Verify every alert payload is redacted and links a valid runbook.
- Review action-item closure from prior postmortems.

## Traceability

Supports `BR-09`, `BR-12`, `FR-15`, `NFR-06`, `NFR-08`, `NFR-11`, `NFR-12`, `NFR-13`, `SR-19`,
gates G3–G5, and all documents in this operations pack.
