# Assumptions and Constraints

Status: Proposed · 2026-11-24

This document separates **assumptions** (believed true, requiring validation) from **constraints**
(true limits for discovery and design) and **open questions** (unresolved decisions).

## Assumptions

| ID | Assumption | Basis | Risk if false | Validation |
| --- | --- | --- | --- | --- |
| A-01 | The primary use case is customer-support ticket answering | `README.md:3-6`, hardcoded order message | Requirements target the wrong workflow | Interview with sponsor |
| A-02 | Tool-calling accuracy matters more than general chat quality | Allowlisted tools and orchestrator design | Over-invest in the wrong evaluation | Interview + dataset review |
| A-03 | A human approves consequential actions | Proposed target in `README.md:208-210` | Approval UX and audit requirements change | Approver interview |
| A-04 | Cloud inference remains available; local inference is evaluated as an alternative | Both provider adapters exist | Provider strategy and budget change | Sponsor + security interview |
| A-05 | 10,000 tickets/day and 1,000/300 tokens are representative planning values | Illustrative model in `README.md:212-215` | Cost and latency targets are meaningless | Volume/data review |
| A-06 | English is the initial evaluation language | Dataset not yet defined | Prompt, token, and quality baselines change | Sponsor interview |
| A-07 | The mock order/customer/FAQ tools resemble production integrations | `src/ai_agent/tools/**` | Tool contract and permissions need redesign | Data-owner interview |
| A-08 | 32,000 context tokens with a 4,000 response reserve are acceptable starting limits | `README.md:92-93` | Prompts/history fail to fit or cost too much | Context measurement |
| A-09 | Conversation history and memory are supporting context, not business authority | `README.md:94-95`, `README.md:116-118` | Incorrect order/permission answers | Threat model + scenario tests |
| A-10 | The staged, documented nature of the project is part of its value | `README.md:3-8`, `LOG.md`, `docs/SUMMARY.md` | Simpler implementation may be preferred | Sponsor interview |
| A-11 | Test fakes and temp SQLite DBs are sufficient for pre-production verification | `README.md:317-318`, `tests/**` | Integration gaps remain invisible | QA/ops review |
| A-12 | A representative ticket dataset can be assembled for evaluation | Evaluation guidance in `README.md:186-188` | Quality targets cannot be measured | Data-owner interview |

## Open questions

| ID | Question | Owner to ask | Blocks |
| --- | --- | --- | --- |
| Q-01 | Is the deliverable a learning prototype, internal pilot, or production channel? | Sponsor | Scope, targets, release gate |
| Q-02 | Who are the end users and who approves consequential actions? | Sponsor / support lead | FR-01, FR-09 |
| Q-03 | Which ticket types, languages, and volume must be represented? | Sponsor / data owner | Evaluation, cost |
| Q-04 | What is the approved budget per ticket and per month? | Sponsor / finance | NFR-04 |
| Q-05 | Which provider/model is approved, and are external data transfers allowed? | Security / compliance | FR-10, NFR-05 |
| Q-06 | Is local Ollama required for privacy, cost, development only, or optional? | Sponsor / platform | FR-10, NFR-03 |
| Q-07 | What hardware is available for local inference? | Platform | FR-13, NFR-02 |
| Q-08 | Which authoritative systems replace the mock tools, and who owns credentials? | Data owner | FR-03, FR-14 |
| Q-09 | How is `owner_id` authenticated and authorized? | Security | FR-05, FR-06, NFR-06 |
| Q-10 | What retention, residency, encryption, and audit rules apply? | Compliance | NFR-05, NFR-08 |
| Q-11 | Which actions are consequential and what evidence must approval show? | Approver / data owner | FR-09 |
| Q-12 | Which interface is canonical: string `ModelClient` or `ModelRequest`/`ModelResponse`? | Maintainer / architect | FR-02, FR-07, FR-10, NFR-09 |

## Constraints

### Technical constraints

- **C-01:** Python 3.12+, `uv`, `pyproject.toml`, and `uv.lock` are the baseline toolchain.
- **C-02:** Runtime dependencies are `openai`, `pydantic`, and `python-dotenv`; `ollama` is not yet
  declared, so the local provider cannot be imported.
- **C-03:** `src/ai_agent/config.py` shadows `src/ai_agent/config/`; generation profiles and the
  model catalog cannot currently be imported.
- **C-04:** Incompatible model interfaces coexist; every new application service must choose the
  canonical contract once `Q-12` is decided.
- **C-05:** Full pytest collection and Ruff currently fail; there is no clean baseline quality gate.
- **C-06:** No HTTP service, API layer, CI/CD, migrations, production database, telemetry stack,
  or typechecker is present.
- **C-07:** Tool data is in-memory mock data; order status, permissions, and workflow state must
  come from authoritative sources before production use.
- **C-08:** Context assembly uses an estimated `ceil(len(text)/4)` token count, not exact provider
  tokenization.
- **C-09:** `ConversationStore` uses SQLite and owner-scoped tables with parameterized queries,
  but no migration layer or production scaling strategy.
- **C-10:** Orchestrator limits are 5 turns and 10 tool calls by default.

### Security and compliance constraints

- **C-11:** `.env` is ignored; API keys and other credentials must never be committed.
- **C-12:** Owner IDs are currently caller-supplied; isolation is not yet backed by authentication.
- **C-13:** Tool results, stored memory, summaries, and retrieved documents are untrusted data.
- **C-14:** Partial streamed JSON must never be treated as a trusted classification result.
- **C-15:** Provider choice must satisfy approved retention, residency, encryption, access, audit,
  and data-terms requirements.
- **C-16:** Local inference requires restricted runtime API access and ownership of hardware,
  updates, monitoring, and scaling.

### Process constraints

- **C-17:** `docs/SUMMARY.md` is lesson-oriented and contains point-in-time status sections; code
  and tests are the stronger evidence of current behavior.
- **C-18:** Historical documents and decisions should be preserved; changed decisions need new ADRs.
- **C-19:** This discovery pack has no interview, telemetry, or measured model-evaluation evidence
  yet; targets must remain labeled as proposed until measured.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Misclassified scope leads to production expectations for a prototype | Rework, missed promises | Resolve `Q-01` before solution design |
| Quality targets are unmeasurable without a dataset | No defensible release decision | Build versioned dataset and evaluation harness first |
| Interface conflict spreads through new code | Provider fallback and tests become fragile | Decide `Q-12` and refactor before new features |
| Missing auth makes owner scoping misleading | Cross-customer data exposure | Define authenticated identity and owner-isolation tests |
| Mock tools are mistaken for authoritative systems | Wrong order/customer answers | Mark tool sources explicitly and gate integration |
| Local provider dependency/config gaps block comparison | No cloud/local evidence | Add dependency, factory, mocked tests, evaluation script |
| Streaming and retry fixes are deferred | Full suite stays red and production behavior unsafe | Treat as release-blocking quality gates |

## Decision gates

- **G1:** Scope, users, volume, and budget confirmed (`Q-01`–`Q-04`).
- **G2:** Canonical model contract and configuration package fixed (`Q-12`, C-03, C-04).
- **G3:** Provider/security policy and data handling approved (`Q-05`, `Q-09`, `Q-10`).
- **G4:** Evaluation dataset, harness, and thresholds agreed (`Q-03`, A-12).
- **G5:** Approval workflow and action list approved (`Q-11`).
