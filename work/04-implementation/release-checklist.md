# Release Checklist

Status: Template · 2026-11-24

Use this checklist for any release candidate. Mark an item complete only when the evidence exists
and is linked. Current blockers are listed first and are unchecked.

## Current blockers

- [ ] Full `uv run pytest -q` collection succeeds (`Iterator`, `LLMValidationError`).
- [ ] `uv run ruff check .` reports zero errors.
- [ ] Canonical model contract recorded in `ADR-004` and applied to all callers.
- [ ] `config.py` / `config/` shadowing resolved.
- [ ] `ollama` dependency declared or provider import safely guarded.
- [ ] Provider capability values and context windows verified, not placeholders.
- [ ] Evaluation dataset and harness frozen; M-01–M-10 measured.
- [ ] Owner scoping, approval gate, and redaction tests pass.

## Code and quality

- [ ] All `BR-xx`, `FR-xx`, `NFR-xx` items in scope are implemented or explicitly waived.
- [ ] Full test suite passes from a clean checkout with no live API keys or model runtime.
- [ ] Lint passes; typecheck passes when configured.
- [ ] Contract suite passes for every configured provider.
- [ ] Architecture rules verified: domain has no infrastructure imports; application has no SDK
      or environment reads.
- [ ] No permanently skipped or excluded failing modules.
- [ ] Code revision, test log, and lint log recorded in release evidence.

## Configuration and secrets

- [ ] `.env` is not committed and no secret appears in the diff or logs.
- [ ] `.env.example` matches all required settings.
- [ ] Missing/invalid configuration produces actionable errors.
- [ ] Provider, model, prompt version, and generation profile are explicit.
- [ ] Local Ollama API is restricted to trusted access if enabled.
- [ ] Dependency lockfile matches `pyproject.toml`.

## Data and security

- [ ] `owner_id` comes from authenticated context and scopes all conversations/memory/tool calls.
- [ ] Owner-isolation tests pass for read, upsert, and delete.
- [ ] Consequential actions require a recorded human approval.
- [ ] Tool results, memory, summaries, and retrieved documents are treated as untrusted data.
- [ ] Logs and traces redact secrets, tokens, and sensitive customer content.
- [ ] Retention, residency, encryption, and audit requirements are approved.
- [ ] Provider data-processing terms are approved.

## Evaluation and evidence

- [ ] Dataset version and holdout split frozen.
- [ ] Prompt version, model ID, provider, generation profile, tool schemas, context limits,
      retry policy, date, and code revision recorded.
- [ ] M-01–M-12 measured or explicitly marked not applicable with owner approval.
- [ ] Classification accuracy ≥ agreed target (proposed ≥95%).
- [ ] Structured-output validity ≥ agreed target (proposed ≥99%).
- [ ] Average latency < agreed target (proposed <2 s) and P95 reported.
- [ ] Cost per ticket/month within approved budget.
- [ ] Regression cases in `../05-evaluation/regression-tests.md` pass.
- [ ] Failure examples and confidence intervals included, not only averages.
- [ ] Cloud and local comparison recorded if both are candidates.

## Observability and operations

- [ ] Trace IDs present on model, tool, retry, context, and approval events.
- [ ] Required metrics emitted: latency, tokens, cost, tool outcome, retries, error class,
      approval decision.
- [ ] Alerts configured for error rate, latency, cost anomaly, and approval failure.
- [ ] Timeouts, cancellation, bounded buffers, and graceful failure verified.
- [ ] Backup/restore or data-recovery procedure tested for durable state.
- [ ] Rollback procedure documented and rehearsed.

## Documentation and decisions

- [ ] README quick start and commands current.
- [ ] `01-discovery`, `02-architecture`, `03-design`, `04-implementation`, `05-evaluation` docs
      updated for changed behavior.
- [ ] ADRs current; new decisions recorded; superseded ADRs preserved.
- [ ] Known gotchas documented where they matter.
- [ ] No sensitive data in docs or examples.

## Sign-off

| Role | Name | Decision | Date | Evidence link |
| --- | --- | --- | --- | --- |
| Product owner |  | Approve / reject / waive |  |  |
| Engineering owner |  | Approve / reject / waive |  |  |
| Security/compliance owner |  | Approve / reject / waive |  |  |
| Operations owner |  | Approve / reject / waive |  |  |

## Release evidence record

| Field | Value |
| --- | --- |
| Release version |  |
| Code revision |  |
| Date |  |
| Provider / model |  |
| Prompt version |  |
| Generation profile |  |
| Dataset version |  |
| Test result |  |
| Lint result |  |
| Evaluation result |  |
| Security result |  |
| Waivers |  |
| Rollback target |  |

## Rollback plan

1. Record the current revision and configuration.
2. Stop new requests if a transport/service is running.
3. Restore the previous revision and configuration from version control.
4. Restore durable state from the tested backup if schema or data changed.
5. Re-run smoke tests and quality gates at the rollback target.
6. Record the incident, cause, decision, and follow-up ADR if a boundary changes.

## Traceability

Supports `BR-09`, `BR-12`, `FR-15`, `NFR-05`, `NFR-06`, `NFR-08`, `NFR-12`, `NFR-13`, and gates
G3–G5 in `../01-discovery/success-metrics.md`.
