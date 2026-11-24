# Business Requirements

Status: Proposed · 2026-11-24

These requirements describe outcomes, not implementation. Priority uses MoSCoW and must be
confirmed with the product owner (`Q-01`). “Evidence” is the repository evidence available at
discovery time, not stakeholder confirmation.

| ID | Requirement | Priority | Evidence | Validation |
| --- | --- | --- | --- | --- |
| BR-01 | Deliver correct, concise answers to customer support messages using authoritative business data | Must | `README.md:3-6`, `src/ai_agent/main.py`, `src/ai_agent/tools/**` | Interview + dataset evaluation |
| BR-02 | Reduce repetitive support work by classifying and routing tickets consistently | Must | `src/ai_agent/application/ticket_classifier.py`, `README.md:157-188` | Interview + classification evaluation |
| BR-03 | Keep humans in control of consequential actions | Must | `README.md:208-210`, `README.md:279-281` | Policy review + approval-flow test |
| BR-04 | Make answers traceable to tool results or validated application state | Must | `README.md:94-95`, `src/ai_agent/application/orchestrator.py:50-55` | Trace review + groundedness evaluation |
| BR-05 | Operate within an approved cost per ticket and monthly budget | Should | `README.md:208-215` cost model | Finance approval + measured token costs |
| BR-06 | Support an approved cloud provider and evaluate local inference as an alternative | Should | `README.md:190-263`, providers in `src/ai_agent/providers/**` | Security approval + comparison experiment |
| BR-07 | Preserve conversation context and relevant owner-scoped facts across turns | Should | `README.md:60-127`, `src/ai_agent/application/conversation_*.py` | Conversation scenario tests |
| BR-08 | Protect customer data, secrets, and owner boundaries | Must | `README.md:23`, `README.md:116-118`, `README.md:255-256` | Threat model + security tests |
| BR-09 | Provide measurable evidence of quality, latency, reliability, and cost before release | Must | `README.md:186-215`, `README.md:313-320` | Evaluation report + CI quality gates |
| BR-10 | Avoid vendor lock-in so models and providers can be changed without rewriting the workflow | Should | `README.md:267-294` dependency inversion guidance | Architecture review + provider swap test |
| BR-11 | Keep the project learnable and maintainable as a staged engineering reference | Should | `README.md:3-8`, `LOG.md`, `docs/SUMMARY.md` | Documentation and onboarding review |
| BR-12 | Fail safely when models, tools, or data are unavailable | Must | Error/retry modules and `README.md:143-155, 147-149` | Failure-injection tests |

## Detailed business requirements

### BR-01 — Trustworthy support answers

**Outcome:** A customer or support agent receives an answer that addresses the issue and is
grounded in the current authoritative order, customer, or FAQ data.

**Business acceptance:** On a representative ticket set, answers meet the agreed correctness,
groundedness, and completion thresholds defined in `success-metrics.md`, with unsupported claims
flagged rather than presented as facts.

**Depends on:** FR-01, FR-02, FR-03, FR-11, NFR-01, NFR-08.

### BR-02 — Consistent classification and routing

**Outcome:** Each ticket is classified into an agreed category with a validated structure so
downstream routing is deterministic.

**Business acceptance:** Classification accuracy and structured-output validity meet the agreed
targets; invalid or incomplete outputs are handled explicitly rather than guessed.

**Depends on:** FR-02, FR-12, NFR-01.

### BR-03 — Human control of consequential actions

**Outcome:** Actions such as refunds, cancellations, account changes, or commitments require
human approval before execution.

**Business acceptance:** The approver role and action list are agreed; no unapproved consequential
action can be executed through a tool.

**Depends on:** FR-06, FR-09, NFR-06.

### BR-04 — Grounded, auditable decisions

**Outcome:** The system can show which tool facts or validated application data supported an
answer.

**Business acceptance:** Conversation history and memory are never accepted as proof of order
status, permissions, or workflow state; review traces are available for sampled tickets.

**Depends on:** FR-03, FR-07, FR-08, NFR-07.

### BR-05 — Cost control

**Outcome:** Per-ticket and monthly cost are understood and stay within an approved budget.

**Business acceptance:** Token usage, retries, infrastructure, and local hardware costs are
reported using the agreed volume model and compared with the approved budget.

**Depends on:** FR-13, NFR-04.

### BR-06 — Provider choice

**Outcome:** The project can run on an approved cloud provider and can evaluate a local provider
without changing the workflow code.

**Business acceptance:** Cloud and local providers pass the same contract tests and are compared
on the same dataset using agreed quality, latency, cost, and capability metrics.

**Depends on:** FR-10, FR-13, NFR-05, NFR-08.

### BR-07 — Useful continuity

**Outcome:** A multi-turn conversation retains relevant context and owner-scoped facts without
treating them as authoritative business state.

**Business acceptance:** Scenario tests show correct reuse of prior context, correction of stale
facts, and no cross-owner leakage.

**Depends on:** FR-04, FR-05, NFR-06.

### BR-08 — Data protection

**Outcome:** Secrets, customer data, conversation history, memory, and logs are handled according
to approved policy.

**Business acceptance:** No secret is committed; owner IDs derive from authenticated context;
retention and access policies are enforced; logs avoid sensitive generated content.

**Depends on:** FR-05, FR-14, NFR-05, NFR-06.

### BR-09 — Evidence before release

**Outcome:** Release decisions are based on measured evaluation and green quality gates.

**Business acceptance:** `success-metrics.md` baselines and targets are filled with measurements;
full tests and lint pass; unresolved blockers are explicitly waived by the owner.

**Depends on:** FR-15, NFR-01, NFR-07, NFR-09.

### BR-10 — Vendor independence

**Outcome:** Providers, models, prompts, and generation profiles are configurable behind stable
interfaces.

**Business acceptance:** Switching between two configured providers requires no change to domain
or orchestration code, and failures can fall back according to policy.

**Depends on:** FR-10, FR-11, FR-13.

### BR-11 — Maintainability and learning value

**Outcome:** New engineers and agents can understand, run, and extend the project without
rediscovering past decisions.

**Business acceptance:** Discovery/spec documents, ADRs for significant decisions, README
commands, and known-gotcha notes are current.

**Depends on:** NFR-10.

### BR-12 — Safe degradation

**Outcome:** Provider errors, invalid output, tool failures, and context overflow produce a
controlled, user-appropriate result.

**Business acceptance:** Failure-injection tests cover timeout, rate limit, malformed JSON,
tool error, and context overflow; no partial streamed JSON is used as a trusted result.

**Depends on:** FR-12, FR-14, NFR-02, NFR-03.
