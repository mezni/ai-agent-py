# Product

Status: Product summary derived from discovery · Proposed targets · 2026-11-24

`ai-agent-py` is a staged customer-support LLM engineering project. Its product goal is to answer
representative support tickets correctly and safely using authoritative business data, with
evidence that another team can reproduce and operate the result.

## Business objectives

| ID | Objective | Priority |
| --- | --- | --- |
| BR-01 | Deliver correct, concise answers grounded in authoritative order/customer/FAQ data | Must |
| BR-02 | Classify and route tickets consistently with validated structured output | Must |
| BR-03 | Keep humans in control of consequential actions | Must |
| BR-04 | Make answers traceable to tool results or validated application state | Must |
| BR-05 | Operate within approved cost per ticket and monthly budget | Should |
| BR-06 | Support an approved cloud provider and evaluate local inference | Should |
| BR-07 | Preserve relevant conversation context and owner-scoped facts across turns | Should |
| BR-08 | Protect customer data, secrets, and owner boundaries | Must |
| BR-09 | Provide measurable quality, latency, reliability, and cost evidence before release | Must |
| BR-10 | Avoid vendor lock-in; change providers without rewriting the workflow | Should |
| BR-11 | Keep the project learnable and maintainable as an engineering reference | Should |
| BR-12 | Fail safely when models, tools, or data are unavailable | Must |

Full definitions and validation methods are in `../01-discovery/business-requirements.md`.

## Users

| User | Need | Current support |
| --- | --- | --- |
| Developer / engineering team | Run and extend a minimal support agent locally | CLI demo and modules; full suite blocked |
| Customer | Receive a correct answer to a support message | Only a hardcoded demo message; no real channel |
| Support agent | Classify/route tickets and inspect grounded facts | Modules exist; not integrated into a workflow |
| Human approver | Approve consequential actions | Not implemented |
| Operator / SRE | Monitor, alert, control cost, recover releases | Observability/deployment specs exist; implementation pending |

## Product scope

### In scope (target)

- One support message in, one validated response out, with usage information.
- Structural classification into agreed categories with complete, schema-valid output.
- Allowlisted tools for order status, customer lookup, and FAQ search with strict arguments.
- Bounded orchestration: turn/tool-call limits, retries, normalized errors, explicit failures.
- Conversation state: SQLite persistence, context budgeting, summary and owner-scoped long-term
  memory treated as untrusted supporting data.
- Provider-neutral model port with OpenAI and optional local Ollama adapters.
- Security controls: authenticated owner IDs, authorization, human approval, redaction, secret
  management.
- Evaluation evidence: M-01–M-12 on a frozen dataset before release.
- Operational controls: logs, metrics, traces, monitoring, alerting, cost budgets, incident
  response.

### Out of scope (today)

- Public HTTP API or user-facing web UI.
- Real integrations to production order/customer/FAQ systems; data is mock today.
- Autonomous refunds, cancellations, or account changes without human approval.
- Multi-tenant SaaS, horizontal scaling, managed database, or cloud-specific provisioning.
- Vision/audio/RAG pipelines and fine-tuning.
- Claimed production quality/cost/latency results; none have been measured.

## Capability status

| Capability | Status | Evidence |
| --- | --- | --- |
| CLI assistant | Partial | `main.py` hardcodes the ticket and prints text/tokens |
| Provider adapter | Partial | `OpenAIProvider.generate()` works; `stream()` broken; Ollama dependency missing |
| Classification | Partial | Classifier, parser, schema and validator exist; validation import broken |
| Tool registry/dispatcher | Partial | Allowlist and strict schemas exist; not integrated with the CLI |
| Orchestration | Partial | `AgentOrchestrator` constructs OpenAI directly and embeds prompt/tool setup |
| Conversation/memory | Partial | SQLite store, managers, summarizer/extractor/retriever exist; not wired to orchestrator |
| Generation profiles/model registry | Partial | Modules exist but `config/` cannot be imported |
| Auth/approval | Gap | No auth layer; `owner_id` caller-supplied; approval not implemented |
| Evaluation | Gap | No dataset, harness, or results |
| CI/CD/deploy/ops | Gap | Specs exist in `../07-deployment/` and `../08-operations/`; no implementation |

## Success criteria

Targets are proposed, not achieved (`../01-discovery/success-metrics.md`):

| Metric | Proposed target |
| --- | --- |
| M-01 classification accuracy | ≥95% |
| M-02 structured-output validity | ≥99% |
| M-05 average latency | <2 s |
| M-06/M-07 P95/TTFT | Owner agreement pending |
| M-08/M-09 tokens and cost | Within approved budget |
| M-10 retry/failure rate | Within agreed error budget |
| M-11 owner-isolation violations | 0 |
| M-12 unapproved consequential actions | 0 |
| M-13/M-14 tests/lint | 100% pass / 0 findings |

## Constraints and open questions

- Python 3.12+, `uv`, OpenAI SDK; local Ollama optional but dependency missing.
- Provider data-processing terms, retention, residency, and approver roles are not confirmed.
- `Q-01`, `Q-09`, `Q-10`, `Q-11`, and `Q-12` remain open or only partially resolved in discovery.
- Any target metric requires a frozen dataset and recorded prompt/model/profile/context/retry
  versions before it can be called a result.

## Traceability

Summarizes `../01-discovery/discovery-brief.md`, `business-requirements.md`,
`functional-requirements.md`, and `success-metrics.md`.
