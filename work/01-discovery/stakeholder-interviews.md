# Stakeholder Interviews

Status: Interview plan and evidence synthesis · No interviews conducted yet · 2026-11-24

This document does not invent interview findings. Roles below are inferred from the codebase,
README, and stated targets; each has a set of questions to confirm or correct the inference.

## Stakeholder map

| Role | Why they matter | Current evidence | Priority |
| --- | --- | --- | --- |
| Product owner / project sponsor | Owns goals, scope, budget, and go/no-go decisions | Staged project structure and proposed targets in `README.md:208-215` | High |
| End customer / ticket submitter | Provides the messages the system must answer | Hardcoded support message in `src/ai_agent/main.py:11` | High |
| Support agent / human approver | Reviews answers and approves consequential actions | “human approval before consequential actions” target in `README.md:208-210` | High |
| Business/application data owner | Owns authoritative order, customer, and FAQ data | Mock data in `src/ai_agent/tools/order_tools.py`, `customer_tools.py`, `knowledge_tools.py`; `README.md:94-95` | High |
| Developer / test maintainer | Builds and verifies components | Prompt registry, fakes, pytest and Ruff commands in `README.md:25-33` | Medium |
| Model / platform engineer | Owns providers, model choice, local runtime, and generation settings | `src/ai_agent/providers/**`, `src/ai_agent/application/model_*.py`, `README.md:157-263` | High |
| Security / compliance owner | Approves provider, retention, access, audit, and data terms | `README.md:206`, `README.md:116-118`, `README.md:255-256` | High |
| Operations / SRE | Owns latency, reliability, cost, logging, and incident response | Production gaps in `docs/SUMMARY.md` and streaming needs in `README.md:147-149` | Medium |

## Interview guide

### Product owner / sponsor

1. What outcome must this project prove: a learning prototype, an internal pilot, or a production
   support channel?
2. What ticket types and volume should the evaluation represent?
3. Which of the proposed targets (95% accuracy, 99% JSON validity, <2 s average latency) are
   contractual and which are aspirational?
4. What is the approved budget per ticket or per month?
5. What would cause the project to be stopped or redesigned?

### End customer / ticket submitter

1. What information do you include when reporting a support issue?
2. Which answers are acceptable without human review?
3. How do you prefer to receive a response: complete text or streamed text?
4. What would make you distrust an automated answer?
5. Which languages and channels must be supported?

### Support agent / human approver

1. Which actions must never be automated without approval?
2. What evidence must an answer show before you approve it?
3. Where do current answers or handoffs fail most often?
4. How much time can be spent reviewing an AI draft?
5. What should happen when a tool or provider fails?

### Business / data owner

1. Which fields in order and customer data are authoritative and which are sensitive?
2. Which tools may the agent call, and with what permissions?
3. What is the source of truth for order status, refunds, and entitlements?
4. How should stale or conflicting tool data be handled?
5. Who approves new tools or changes to tool schemas?

### Model / platform engineer

1. Is cloud inference mandatory, optional, or prohibited for production?
2. Which models are approved and what capabilities are required?
3. What hardware is available for local Ollama inference?
4. How should provider fallback and rate limits behave?
5. Which generation profile and model-selection policy should be tested first?

### Security / compliance owner

1. What data may be sent to an external provider, and under what terms?
2. What retention, residency, encryption, and audit rules apply to conversations and memory?
3. How must `owner_id` be derived and authorized?
4. How should tool results and stored memory be treated as untrusted input?
5. What secrets management and key rotation process applies?

### Operations / SRE

1. What availability and latency targets apply at expected volume?
2. Which metrics, logs, traces, and alerts are required?
3. How are retries, timeouts, circuit breakers, and rate limits expected to behave?
4. What deployment model is allowed: CLI, service, container, or managed runtime?
5. What incident and rollback process applies after a bad prompt or model change?

### Developer / test maintainer

1. Which interface should be canonical: string-based `ModelClient` or
   `ModelRequest`/`ModelResponse`?
2. Which quality gates must be green before merging?
3. What fixture and fake strategy keeps tests provider-independent?
4. How should prompt, model, and tool changes be versioned and reviewed?
5. Which documentation is required for future engineers and agents?

## Evidence-backed findings so far

| Topic | Observed signal | Interpretation to validate |
| --- | --- | --- |
| User surface | CLI prints one hardcoded answer | There is no confirmed interactive user workflow yet |
| Authority | `README.md:94-95` says history and memory are not authoritative business state | Stakeholders likely expect tool-grounded answers, but this needs confirmation |
| Approval | Human approval is a target, not implemented | The approval point and approver role are undefined |
| Provider choice | Both OpenAI and Ollama adapters exist, neither fully wired | Provider policy is unresolved |
| Ownership | `owner_id` is caller-supplied in `conversation_store.py` | Identity and authorization design is missing |
| Quality | No measured evaluation results exist | Stakeholders may not agree on the evaluation dataset |

## Hypotheses to validate

- **H-01:** The primary user is a support agent who reviews drafts, not the end customer.
- **H-02:** Tool-calling correctness matters more than open-ended conversational quality.
- **H-03:** Local inference is desired for development/privacy, while cloud remains an option.
- **H-04:** Consequential actions are rare but high-risk, so a human gate is mandatory.
- **H-05:** The 32,000-token context and 4,000-token response reserve are acceptable initial limits.
- **H-06:** The mock order, customer, and FAQ tools are representative of production integrations.

## Synthesis rules

- Record each interview with date, role, interviewer, and explicit consent for note-taking.
- Quote participants only with permission; otherwise record paraphrases and confidence.
- Map every new need to a `BR-xx`, `FR-xx`, or `NFR-xx` or mark it as out of scope.
- Conflicting answers become open questions, not silent averages.
- Update `discovery-brief.md`, requirements, and `assumptions-and-constraints.md` together.
