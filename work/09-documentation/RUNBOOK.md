# Runbook

Status: Operational procedures · Target until implementation exists · 2026-11-24

## Procedure template

1. Record incident/change ID, UTC time, environment, revision, provider/model/profile, and owner.
2. Contain before diagnosing; preserve redacted evidence.
3. Take the least risky action from the relevant procedure.
4. Verify with startup validation, smoke tests, migration status, and monitoring.
5. Record decision, impact, follow-ups, and ADR if a boundary changed.

Use `../08-operations/incident-response.md` for roles and evidence rules. Never paste secrets,
tickets, prompts, model outputs, tool payloads, or raw customer IDs into records.

## Startup or configuration failure

1. Read the error; confirm which variable/setting is missing or invalid.
2. Verify environment-specific config from `../07-deployment/environment-configuration.md`.
3. Confirm secrets are injected from the secret store, not committed files.
4. Do not default to a placeholder model/provider or `context_window=0`.
5. Re-run startup validation; if deployment fails, stop promotion and inform engineering owner.

## Full test/lint failure

1. Reproduce locally: `uv run pytest -q`, `uv run ruff check .`.
2. Check known blockers in `DEVELOPMENT.md`: `Iterator`, `LLMValidationError`, `config.py` shadowing,
   missing `ollama`.
3. Fix the smallest root cause, add a regression test, and re-run full checks.
4. Block promotion until gates pass or an approved waiver exists.

## Provider outage or error spike

1. Check `provider_errors_total`, retry attempts, error class, latency, and budget.
2. Stop retry storms; confirm bounded backoff and `retry_after` handling.
3. Verify provider status/credentials/quota; do not print keys.
4. Do not silently fall back to another provider (`ADR-005` pending).
5. If approved alternate exists, pin provider/model/profile explicitly and record decision.
6. Monitor error rate and cost after recovery.

## Slow responses / latency spike

1. Check M-05 average, M-06 P95, M-07 TTFT, provider latency, and retries.
2. Inspect traces for `context.build`, `model.generate`, `tool.dispatch`, and retry events.
3. Verify context limits and response reserve; remove only non-authoritative history/memory.
4. Compare current generation profile/model with last known-good release.
5. Roll back config/model/profile if the change correlates; record evidence.

## Tool failure spike

1. Check tool name, validation result, outcome, and error class metrics.
2. Confirm tool is allowlisted and arguments match the strict schema.
3. Inspect redacted trace IDs; do not inspect raw tool payloads in alerts/docs.
4. Deny unknown/unauthorized tools; fix schema/handler with tests.
5. Verify no consequential action executed without approval.

## Cost spike

1. Check cost by environment/provider/model/profile, token directions, retries, and revision.
2. Pause the expensive channel/tenant/path if approved.
3. Confirm price table/currency and reconciliation with provider billing.
4. Review context budgeting, profile token caps, caching policy, and model mix.
5. Restore budget; compare quality/latency before keeping an optimization.

## Migration failure

1. Stop CLI/batch writes and new traffic if a service exists.
2. Record `schema_migrations` version/name/checksum and backup location.
3. Read migration logs; do not rerun blindly.
4. On a restored copy, retry or validate the migration.
5. Apply the approved down migration only if verified; otherwise restore the pre-migration backup.
6. Run `PRAGMA integrity_check`, `foreign_key_check`, verification queries, and smoke tests.
7. Record outcome and inform data owner. Details: `../07-deployment/database-migrations.md`.

## Application rollback

1. Identify last known-good artifact, config, provider/model/prompt/profile, and schema version.
2. Pause new work/traffic; preserve failed artifact and logs.
3. Redeploy previous immutable image/config; never rebuild from a moving branch.
4. Roll back schema only with verified down migration/backup.
5. Run readiness, smoke tests, owner-isolation check, migration status, and monitoring watch.
6. Record incident and follow-ups. Details: `../07-deployment/rollback-strategy.md`.

## Secret exposure

1. Revoke/rotate the credential immediately; disable affected deployment/job.
2. Identify exposure window and environments; preserve logs/artifacts as evidence.
3. Search repository, CI artifacts, logs, traces, and backups for the value.
4. Replace secret via secret store; verify all consumers and secret scans.
5. Treat as P1 and follow incident process. Details: `../06-security/secrets-management.md`.

## Owner-isolation or approval failure

1. Disable the affected route/tool; preserve audit/log/trace evidence.
2. Treat as P1; assign security owner and incident commander.
3. Identify affected records/actions and whether consequential work executed.
4. Roll back code/config; require passing cross-owner and approval tests before re-enable.
5. Document impact and required notifications. Details: `../06-security/access-control.md`.

## Prompt-injection or data leakage concern

1. Disable the affected tool/source or untrusted data path.
2. Preserve redacted traces/logs; do not copy raw content into tickets/docs.
3. Verify untrusted data was treated as data, not instructions.
4. Add a regression fixture from the sanitized pattern; re-run security tests.
5. Re-enable only after G4-equivalent checks pass.

## Backup restore / data corruption

1. Stop writes immediately; declare P1.
2. Identify latest verified backup and corruption scope.
3. Restore to an isolated copy first; run integrity/foreign-key checks and row-count checks.
4. Restore target only with data/product owner approval.
5. Replay only verified events; keep failed-state evidence.
6. Verify application version matches restored schema.

## Monitoring or alert blind spot

1. Switch to manual watch and assign an owner.
2. Check log/metric/trace presence and exporter health.
3. Re-enable alerts with redacted evidence; test firing and recovery paths.
4. Record detection gap in postmortem.

## Traceability

Implements `../08-operations/alerting.md`, `incident-response.md`, `monitoring.md`, and
`../07-deployment/rollback-strategy.md`.
