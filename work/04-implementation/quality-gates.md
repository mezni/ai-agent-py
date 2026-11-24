# Quality Gates

Status: Proposed enforcement · 2026-11-24

## Purpose

Quality gates turn the targets in `../01-discovery/success-metrics.md` into enforceable checks. A
gate passed without its evidence artifact is not passed.

## Gate sequence

| Gate | Name | Exit criteria | Evidence |
| --- | --- | --- | --- |
| G0 | Local baseline (working checkpoint) | Tests collect; baseline pass/fail recorded; Ruff findings listed | `baseline-report.md` or CI artifact |
| G1 | Discovery | Sponsor confirms scope, users, volume, budget, providers, approval roles; `Q-01`–`Q-12` resolved or waived | Updated discovery docs + sign-off |
| G2 | Foundation | Canonical contract chosen; config package importable; full tests and lint pass | ADR-004, CI test/lint logs |
| G3 | Evaluation | Frozen dataset and harness; M-01–M-10 measured for at least one cloud and one local candidate; cost model approved | `../05-evaluation/evaluation-results.md` |
| G4 | Safety | Owner isolation, approval gate, untrusted-data handling, redaction tests pass; provider/security approval recorded | Security test report + approval record |
| G5 | Acceptance | M-01–M-12 meet agreed thresholds on holdout data; docs and ADRs current | Release report + checklist |

G0 is an implementation checkpoint used before merging refactors; G1–G5 are the discovery exit
gates and must not be renumbered.

## Checks

| Check | Command / method | Threshold | Current status | Blocks |
| --- | --- | --- | --- | --- |
| Full tests | `uv run pytest -q` | 0 failures, 0 collection errors | Failing: 2 collection errors; 57 pass when excluded | G0, G2, G5 |
| Lint | `uv run ruff check .` | 0 errors | 8 errors | G0, G2, G5 |
| Typecheck | Agreed tool when configured | 0 errors | Not configured | G2 (proposed) |
| Config imports | Smoke import of settings/profiles/catalog | All succeed | Profiles/catalog unimportable | G2 |
| Contract suite | Shared provider tests | All adapters pass | Missing contract suite | G2, G3 |
| Architecture rules | Dependency import check | Domain clean; app has no SDK/env reads | Violations in orchestrator/classifier | G2 |
| Classification quality | Evaluation harness | ≥95% accuracy (proposed) | Unmeasured | G3, G5 |
| Structured validity | Evaluation harness | ≥99% validity (proposed) | Unmeasured | G3, G5 |
| Latency | Instrumented traces | <2 s average (proposed); P95 agreed | Unmeasured | G3, G5 |
| Cost | Usage × prices + infrastructure | Within approved budget | Model only, unmeasured | G3, G5 |
| Tool correctness | Scenario suite | Agree threshold with owner | Unmeasured | G3, G5 |
| Owner isolation | Security tests | 0 cross-owner reads/writes/deletes | No auth layer; untested | G4 |
| Approval gate | Failure-injection tests | 0 unapproved consequential actions | Not implemented | G4 |
| Redaction | Log capture tests | No secrets/sensitive content in logs | Not implemented | G4 |
| Documentation | Review checklist | README/specs/ADRs current | Partial | G5 |

## Current blockers

| Blocker | Owner | Required fix | Gate |
| --- | --- | --- | --- |
| `Iterator` undefined / incomplete `stream()` | Provider owner | Import and implement stream events | G0, G2 |
| `LLMValidationError` undefined | Application owner | Define error and update catalog/tests | G0, G2 |
| `config.py` shadows `config/` | Platform owner | Convert to package | G2 |
| `ollama` dependency missing | Platform owner | Declare dependency or guard import | G3 |
| Two model contracts | Architect | Decide `Q-12`, record `ADR-004`, migrate | G2 |
| No auth/approval/audit | Security owner | Implement and test controls | G4 |
| No measured evaluation | Evaluation owner | Freeze dataset and run harness | G3, G5 |

## Threshold policy

- Targets in discovery are proposals until the sponsor confirms them.
- A threshold cannot be lowered in the report; it must be changed in `success-metrics.md` with an
  owner, date, and rationale.
- “Unmeasured” is not “passed”.
- Any waiver requires the gate owner, affected requirement ID, expiry date, and mitigation.

## Evidence artifacts

| Artifact | Location | Produced by |
| --- | --- | --- |
| Test log | CI run artifact or `work/04-implementation/reports/` | CI |
| Lint log | CI run artifact or reports directory | CI |
| Evaluation results | `../05-evaluation/evaluation-results.md` | Evaluation harness |
| Dataset version | `../05-evaluation/evaluation-dataset.jsonl` | Dataset owner |
| Regression cases | `../05-evaluation/regression-tests.md` | Test owner |
| ADR index | `../02-architecture/architecture-decisions.md` | Architect |
| Security approval | Release record | Security/compliance owner |

## CI enforcement sequence

1. Install locked dependencies.
2. Run lint.
3. Run full test suite.
4. Run architecture/import-boundary check when configured.
5. Build evaluation report from frozen dataset when harness exists.
6. Run security regression suite when implemented.
7. Publish artifacts and fail the build if any blocking gate fails.

## Definition of green

A build is green only when:

- all blocking checks passed from a clean checkout;
- no required evidence artifact is missing;
- no waiver has expired;
- the code revision is recorded with the results.

## Traceability

Supports `BR-09`, `FR-13`, `FR-15`, `NFR-01`, `NFR-02`, `NFR-04`, `NFR-06`, `NFR-12`, `NFR-13`,
and the exit gates in `../01-discovery/success-metrics.md`.
