# Discovery Brief

Status: Draft · 2026-11-24

## Problem statement

Customer support work requires reading a customer's message, understanding the issue, checking
authoritative systems, and replying accurately. Today `ai-agent-py` demonstrates only a single
provider-backed answer: the CLI sends one hardcoded support message and prints the response and
token counts (`README.md:3-6`, `src/ai_agent/main.py`). The richer capabilities needed for a
trustworthy support assistant — classification, tools, conversation state, memory, streaming,
provider choice, and evaluation — exist as staged modules but are not yet a coherent,
measurable product.

## Vision

A layered Python support agent that can hold a multi-turn conversation, classify and validate
requests, call a small allowlisted set of authoritative tools, use owner-scoped memory as
supporting context, stream responses, switch between approved cloud and local providers, and
operate within measured quality, latency, cost, and safety limits.

## Current state (observed)

| Area | Observed state | Evidence |
| --- | --- | --- |
| User surface | One-shot CLI with a hardcoded message | `src/ai_agent/main.py`, `README.md:10-36` |
| Model access | OpenAI Responses API, 30 s timeout, SDK retries, token usage normalized | `src/ai_agent/providers/openai_provider.py` |
| Classification | Strict Pydantic output, parser, validation, retry concepts exist | `src/ai_agent/application/ticket_classifier.py`, `tests/domain/test_ticket_classification.py` |
| Tools | Allowlisted registry, strict argument schemas, dispatcher, mock order/customer/FAQ data | `src/ai_agent/tools/**` |
| Orchestration | 5-turn / 10-tool-call loop exists but constructs OpenAI directly | `src/ai_agent/application/orchestrator.py`, `README.md:289-294` |
| Conversation | SQLite store, token-budget context manager, conversation facade | `src/ai_agent/application/conversation_*.py`, `README.md:60-98` |
| Memory | Summarizer, deterministic extractor, retriever, manager, owner-scoped facts | `src/ai_agent/application/memory_*.py`, `README.md:100-127` |
| Streaming | Contract and test exist; provider `stream()` is broken | `README.md:129-155`, `src/ai_agent/providers/openai_provider.py` |
| Model choice | Frozen definitions, registry, selector, profiles, catalog exist but are not importable/wired | `README.md:157-226`, `src/ai_agent/config.py`, `src/ai_agent/config/` |
| Local inference | Ollama provider written; dependency, factory, config, and tests missing | `README.md:228-263`, `src/ai_agent/providers/ollama_provider.py` |
| Quality gates | 57 tests pass when two broken modules are excluded; Ruff reports 8 errors | `README.md:313-320`, `tests/**` |

## Desired outcome

1. A working end-to-end support flow from user message to validated, grounded response.
2. A single, consistent model-client contract used by every provider and application service.
3. Measured quality, latency, token usage, and cost on a representative ticket dataset.
4. Explicit safety boundaries: allowlisted tools, authorized owner IDs, human approval for
   consequential actions, and untrusted-data handling for tool results and memory.
5. An operable development and deployment path with observable failures and reproducible tests.

## Scope

### In scope for discovery

- Customer-support ticket answering and classification
- Tool-grounded order, customer, and FAQ lookup
- Multi-turn conversation state and owner-scoped long-term memory
- Cloud and local model providers behind one interface
- Streaming delivery, generation settings, model selection, retries, and failure paths
- Evaluation, observability, cost, security, and human-approval requirements

### Out of scope for discovery

- Building a full support-platform UI or public API product
- Training or fine-tuning custom models
- Implementing production authentication, billing, or ticket-management systems
- Multi-language support beyond what the dataset proves
- Parallel tool execution and automatic history summarization (deferred)

## Key findings

| Finding | Impact |
| --- | --- |
| Two incompatible `ModelClient` interfaces coexist | Blocks clean provider substitution, fallback, and testing |
| `config.py` shadows the `config/` package | Generation profiles and model catalog cannot be imported |
| Full pytest collection is blocked by `Iterator` and `LLMValidationError` errors | No reliable quality gate today |
| Orchestrator bypasses dependency inversion | Hard to test, switch providers, or enforce central policy |
| No evaluation dataset or measured model results exist | Proposed 95%/99%/2 s targets are unvalidated |
| Owner IDs are caller-supplied and no auth layer exists | Owner isolation is not yet an authorization guarantee |
| Memory and conversation components are not integrated with the orchestrator | Multi-turn behavior is not available to users |

## Open questions

See `assumptions-and-constraints.md` for `A-xx` and `Q-xx`. The most urgent:

- Who is the actual product owner and who approves consequential actions?
- Which provider/model is approved for production, and is local inference required or optional?
- What is the expected ticket volume, ticket mix, acceptable cost per ticket, and language set?
- What data retention and residency rules apply to conversations, memory, and logs?
- Which systems must tools call in production, and who owns their credentials?

## Decision gates

| Gate | Decision required | Evidence needed |
| --- | --- | --- |
| G1 | Confirm product owner, users, and support workflow | Stakeholder interviews |
| G2 | Choose the canonical `ModelClient` contract | Architecture review + tests |
| G3 | Select provider/model and generation profiles | Dataset evaluation results |
| G4 | Approve production security boundary | Threat model, auth design, provider terms |
| G5 | Accept the end-to-end flow | Contract, integration, and evaluation results |

## Next steps

1. Validate stakeholder roles and answers to `Q-01`–`Q-12`.
2. Repair the test/lint blockers and establish a trustworthy baseline.
3. Define the canonical model-client contract and provider factory.
4. Build a representative ticket dataset and evaluation harness.
5. Wire the orchestrator, conversation, memory, and streaming paths behind that contract.
