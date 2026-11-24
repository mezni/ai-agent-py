# Rollback Strategy

Status: Deployment recovery procedure · 2026-11-24

## Policy

Every release must have a recorded rollback target before promotion. Rollback restores a previously
known-good combination of code artifact, configuration, provider/model/prompt settings, and schema
version. Partial rollback is allowed only when compatibility is verified.

Prefer forward fixes for low-risk changes. Roll back immediately when a release causes data
corruption, owner-isolation failure, secret exposure, security-control failure, unavailable critical
path, or budget/alert breach.

## Rollback matrix

| Failure | Rollback action | Data action | Approval |
| --- | --- | --- | --- |
| Bad application code/config | Redeploy previous image/tag and config | None | Engineering owner |
| Bad provider/model/profile | Restore previous settings from release record | None | Engineering owner; provider owner if terms change |
| Bad prompt/tool schema | Restore previous versioned prompt/schema | None | Evaluation owner if quality affected |
| Migration failure before completion | Restore prior schema version or backup | Restore backup from before migration | Engineering + data owner |
| Data corruption after migration | Stop writes; restore tested backup; replay only verified events | Backup restore | Product + data + engineering owner |
| Security/secret exposure | Disable affected deployment/key; revoke/rotate | Preserve evidence, do not scrub logs prematurely | Security owner |
| Owner-isolation failure | Disable service path; roll back code/config | Audit affected records | Security + product owner |
| Evaluation regression | Restore previous artifact/settings | None if no durable change | Evaluation owner |

## Information to record first

| Field | Source |
| --- | --- |
| Failed release version and code revision | Release record / CI artifact |
| Failed image tag/digest and schema version | Registry / `migrations status` |
| Provider, model, prompt, generation profile, feature flags | `environment-configuration.md` record |
| Last known-good release and schema version | Prior release record |
| Backup location and verification result | Operations log |
| Incident/trace ID | Observability system |

## Procedure

1. **Contain.** Pause new CLI/batch work or stop traffic to the service endpoint if one exists.
   Do not start new migrations or provider jobs.
2. **Decide.** Use the matrix above and record the decision, owner, and timestamp.
3. **Code/config.** Redeploy the previous immutable image/config; never rebuild from a moving branch.
   Keep the failed artifact for investigation.
4. **Schema/data.** If schema changed, run the tested down migration only if approved and verified;
   otherwise restore the backup taken before the migration. Confirm `schema_migrations` matches the
   rollback target.
5. **Provider/prompt.** Restore settings from the release/evaluation record. Do not fall back to a
   provider with unapproved data terms.
6. **Verify.** Run startup validation, smoke tests, lint/test evidence check for the rollback
   revision, migration status, owner-isolation smoke test, and one end-to-end ticket/classification
   path.
7. **Monitor.** Watch error rate, latency, cost, approval failures, and failed logins for an agreed
   observation window.
8. **Close.** Record incident cause, rollback steps, evidence, and follow-up ADR/issue.

## Compatibility rules

- New code must read the old schema during expansion phases (`database-migrations.md`).
- Old code must tolerate additive schema changes until contraction is deployed.
- Down migrations that drop/transform data require a verified backup; they are not automatic.
- Configuration rollback must include feature flags and generation profiles, not only secrets.
- If provider/model rollback changes quality, restore the recorded prompt and dataset version too.
- Never roll back to a revision missing a security fix without an explicit risk acceptance.

## Rehearsal checklist

- [ ] Previous image tag retained and deployable.
- [ ] Backup restore rehearsed in staging with the current schema.
- [ ] Down migration rehearsed where supported.
- [ ] Config/provider/prompt restore rehearsed.
- [ ] Smoke tests and owner-isolation test run at rollback target.
- [ ] Rollback time measured and compared with the recovery objective.
- [ ] Failed artifact and logs retained for incident review.
- [ ] Release record lists rollback target before promotion.

## Current limitations

No deployed service, registry, backup job, migration runner, or automated rollback exists today.
The current CLI can be rolled back by checking out the prior revision and re-running
`uv sync --frozen`; durable SQLite state must be preserved separately. This procedure becomes an
operational requirement when deployment automation is introduced.

## Traceability

Aligns with `../04-implementation/release-checklist.md`, `ci-cd.md`,
`database-migrations.md`, `../06-security/secrets-management.md`, `BR-09`, `BR-12`, `FR-15`,
`NFR-06`, `NFR-08`, `NFR-12`, and gates G3–G5 in `../01-discovery/success-metrics.md`.
