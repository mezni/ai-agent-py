# CI/CD

Status: Proposed pipeline · No workflows exist today

## Current state

There is no `.github/` workflow, CI configuration, deployment job, or release artifact pipeline.
Verification is manual:

- `uv run pytest -q` — currently fails collection on `Iterator` and `LLMValidationError`.
- `uv run ruff check .` — currently reports 8 errors.
- `uv run ai-agent-py` — one-shot CLI, not a deployable service.

## Target pipeline stages

| Stage | Command / action | Gate | Artifact |
| --- | --- | --- | --- |
| Install | `uv sync --frozen` | Dependency lock consistent | Environment |
| Lint | `uv run ruff check .` | 0 errors | Lint log |
| Test | `uv run pytest -q` | 0 failures/collection errors | Test report |
| Config smoke | Import settings, profiles, catalog | All import; no secret echoed | Smoke log |
| Architecture | Dependency-boundary check | Domain clean; app has no SDK/env reads | Check report |
| Security | Secret scan, dependency scan, redaction tests | 0 critical findings | Security report |
| Build | `docker build -t ai-agent-py:$SHA .` | Build succeeds | Image digest |
| Evaluation | Frozen dataset harness | M-01–M-10 reported or waived | Evaluation report |
| Deploy staging | Promote same image/config | G2–G4 passed | Deployment record |
| Deploy production | Approved promotion | G5 + sign-off | Release record |

Test/lint/build stages run on every pull request. Deployment stages run only on approved release
tags after gates pass.

## Promotion model

| Environment | Trigger | Credentials | Data | Approval |
| --- | --- | --- | --- | --- |
| Development | Local or PR build | Dummy/test keys | Synthetic tickets | Developer |
| CI validation | Every PR | Dummy keys; no live provider | Synthetic fixtures | Automated |
| Evaluation | Tagged candidate | Controlled evaluation credentials | Frozen sanitized dataset | Evaluation owner |
| Staging | Release candidate | Staging secrets | Sanitized/temporary DB | Engineering owner |
| Production | Approved release | Production secrets from secret manager | Production DB with backup | Sponsor + security owner |

Never reuse production credentials in CI or evaluation jobs.

## Proposed workflow skeleton

```yaml
name: validate
on:
  push:
    branches: [main]
  pull_request:
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run pytest -q
      - run: uv build
```

This skeleton is illustrative and must be reviewed/approved before adding it. Deployment jobs,
secret references, environment protections, and evaluation artifacts are intentionally omitted.

## Secrets in CI

- Use platform secret store with masked values and environment-scoped access.
- Unit tests must use dummy values from `tests/conftest.py` and never call live APIs.
- Evaluation jobs may use controlled credentials only with approved provider/data terms.
- Do not print environment dumps, full prompts, model responses containing PII, or SDK error bodies.
- CI artifacts must not include `.env`, secrets, raw customer data, or unmasked evaluation records.
- Rotate credentials exposed to a job after any suspected leak (`../06-security/secrets-management.md`).

## Artifacts and versioning

| Artifact | Requirement |
| --- | --- |
| Image | Tagged with commit SHA; registry retains prior tag for rollback |
| Test/lint logs | Attached to the run and release record |
| Evaluation report | Dataset/model/prompt/profile versions and code revision recorded |
| Migration scripts | Versioned with the release and verified on a copy of production-like data |
| Release record | Links all artifacts, approvals, and waivers |

## Quality-gate enforcement

The pipeline must fail when any blocking check fails:

- full tests and lint;
- config/profile/catalog imports;
- architecture/dependency rules when configured;
- secret and dependency scans;
- G4 safety tests;
- G5 evaluation thresholds, unless an unexpired waiver is recorded.

“Unmeasured” does not pass a gate. Waivers require owner, requirement ID, expiry, and mitigation.

## Current blockers before CI can be green

- `Iterator` undefined / incomplete `stream()`.
- `LLMValidationError` undefined.
- `config.py` shadows `config/`.
- `ollama` dependency missing or unguarded.
- No contract suite, security tests, evaluation harness, or image build.

## Traceability

Supports `BR-09`, `FR-15`, `NFR-11`, `NFR-12`, `NFR-13`, gates G2–G5 in
`../04-implementation/quality-gates.md`, and `../04-implementation/testing-strategy.md`.
