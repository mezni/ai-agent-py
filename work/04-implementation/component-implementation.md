# Component Implementation Guide

Status: Current and target · 2026-11-24

This document is the implementation checklist for each component. “Done” requires working code,
tests, and updated specs — not merely a file existing.

## Component summary

| Component | Files | Current | Target change | Traces |
| --- | --- | --- | --- | --- |
| Configuration | `config.py`, `config/` | Settings works; profiles/catalog unimportable | Importable package, validated settings, single source | `FR-10`, `NFR-11` |
| Model contract | `application/model_client.py`, `domain/models.py` | Two conflicting interfaces | One canonical port (`Q-12`, pending ADR-004) | `FR-02`, `FR-07`, `FR-10` |
| Provider adapters | `providers/openai_provider.py`, `ollama_provider.py` | OpenAI partial; Ollama not importable | Shared contract, factory, error mapping, usage | `FR-07`, `FR-10`, `FR-13` |
| Assistant | `application/assistant.py` | Two classes use different contracts | One assistant on canonical port | `FR-01`, `FR-07` |
| Classifier | `application/ticket_classifier.py` | Direct SDK/env; parse + validate | Injected prompt/model/parser/validator/retry | `FR-02`, `ADR-002` |
| Parser/validator | `response_parser.py`, `ticket_validation.py` | Parser OK; validator import broken | Complete error taxonomy and business rules | `FR-02`, `ADR-003` |
| Retry/errors | `errors.py`, `retry.py` | Taxonomy incomplete; inconsistent use | One classified policy across call sites | `FR-12`, `FR-15` |
| Orchestrator | `application/orchestrator.py` | Direct SDK/env/prompt/registry | Injected collaborators; approval; bounded loop | `FR-03`, `FR-04`, `FR-09` |
| Prompts | `prompts/**` | v1/v2 registry; builder pinned to v1 | Injected builder; selected version from config | `FR-08`, `FR-11` |
| Tools | `tools/**` | Registry/dispatcher/schemas; mock data | Injected registry, auth, approval, typed results | `FR-03`, `FR-14` |
| Conversation | `conversation_manager.py`, `context_manager.py`, `conversation_store.py` | Implemented; not wired | Owner scoping and orchestration integration | `FR-05`, `FR-06` |
| Memory | `memory_*.py`, `llm_memory_summarizer.py` | Components exist; not wired | Retrieval in context; triggers; owner isolation | `FR-06`, `FR-14` |
| Generation/model choice | `generation_*.py`, `model_*.py`, `config/**` | Not imported/wired | Provider mapping and measured selection | `FR-08`, `FR-13` |
| CLI/composition | `main.py` | Hardcoded input, direct construction | Parse input, inject all dependencies, clear errors | `FR-01`, `FR-15` |
| Observability | None structured | Prints text/tokens only | Metrics/logs/traces with redaction | `FR-15`, `NFR-13` |

## Configuration

**Current:** `Settings` reads `OPENAI_API_KEY` and `OPENAI_MODEL` at import time; `config.py`
shadows `config/`.

**Implement:**

- Make `src/ai_agent/config/` a package with `__init__.py` and a typed settings module.
- Validate required values on startup, with a clear message listing missing variables.
- Load profiles/catalog from that package.
- Pass settings into the composition root; do not read `os.environ` in application modules.

**Done when:** profiles and catalog import in a clean environment, missing config yields an
actionable CLI error, and no secret appears in logs or errors.

## Model contract and providers

**Current:** string-based `ModelClient.generate(prompt: str) -> str` /
`stream(prompt: str) -> Iterator[str]` coexists with `ModelRequest`/`ModelResponse`. The OpenAI
stream method references undefined `Iterator` and `self.model`; Ollama lacks a declared dependency.

**Implement:**

- Decide the canonical contract and record it in `ADR-004`.
- Implement it in both adapters; keep SDK events, generation options, and error translation inside
  providers.
- Add a provider factory that selects from validated settings and verifies required capabilities.
- Normalize provider errors into the application error taxonomy with sanitized messages.
- Preserve usage data for cost/latency metrics.

**Done when:** both providers pass the same contract suite, unit tests need no live runtime, and
application code has no SDK imports.

## Assistant

**Current:** `CustomerSupportAssistant.answer()` returns `ModelResponse`; `Assistant.ask()`/
`ask_stream()` use the string contract.

**Implement:** one assistant API spanning non-streaming and streaming paths. Keep a reliable
non-streaming answer path for classification and validation.

**Done when:** one interface is used everywhere and callers no longer depend on which class was
chosen.

## Classification and structured output

**Current:** classifier constructs `OpenAI`, reads `OPENAI_MODEL`, calls `responses.parse`, then
parses and validates. `ticket_validation.py` imports undefined `LLMValidationError`.

**Implement:** inject prompt builder, model client, parser, validator, and retry policy; use prompt
v1 or v2 explicitly; apply strict schema and business rules; route invalid/failed results to a
controlled fallback.

**Done when:** classifier tests use fakes and cover success, refusal, incomplete, malformed,
extra-field, invalid-business-value, retry, and exhaustion cases.

## Retry and error taxonomy

**Current:** `LLMError` hierarchy defines transient/permanent/response errors; `retry.py` retries
`LLMTransientError` with jitter and optional `retry_after`; other modules use unrelated exceptions.

**Implement:** add missing validation/tool/context/approval errors, map provider SDK exceptions to
the hierarchy, and use one `execute_with_retry` policy at all call sites. Preserve injectable sleep.

**Done when:** each catalog entry in `error-catalog.md` has a test, a retry decision, and a
sanitized user-facing outcome.

## Orchestrator

**Current:** direct `OpenAI` construction, `OPENAI_MODEL` reads, embedded prompts, self-built
registry, broad exception handling, 5-turn/10-tool-call limits.

**Implement:** inject model client, prompt builder, parser/validator, tool registry/dispatcher,
store/conversation/memory collaborators, approval gate, and telemetry. Execute consequential tools
only after approval.

**Done when:** a full tool-grounded scenario passes with fakes; loop-limit, invalid-tool,
provider-error, and denied-approval cases are tested.

## Prompts

**Current:** frozen `PromptTemplate`, duplicate-checking `PromptRegistry`, v1/v2 ticket prompts,
builder pinned to v1.

**Implement:** inject the registry/builder; select version from configuration; record prompt version
in evaluation and traces.

**Done when:** changing prompt version requires no code edit and evaluation reports include the
version.

## Tools

**Current:** allowlisted registry, strict Pydantic argument models, JSON dispatcher, `ToolResult`
envelope, in-memory mock data. Dispatcher converts all handler errors to `ToolExecutionError`.

**Implement:** inject registry/dispatcher; add authorization and approval before handler execution;
replace broad exception handling with classified errors; keep tool results as untrusted data.

**Done when:** unknown tools, extra arguments, malformed JSON, and denied approvals never reach a
handler, and each outcome is testable.

## Conversation and memory

**Current:** SQLite store with four tables, owner-scoped facts, token-budget context builder,
manager facades; no owner on conversations and no orchestrator integration.

**Implement:** add owner identity, scope all queries, assemble target context order, add automatic
summarization triggers, wire into orchestrator, and treat retrieved facts as untrusted context.

**Done when:** multi-turn and owner-isolation tests pass and memory never overrides instructions
or business authority.

## Generation and model selection

**Current:** frozen configs/builder/registry/selector exist but cannot be imported from `config/`;
catalog uses placeholder IDs and `context_window=0`.

**Implement:** importable profiles, provider option mapping, verified capabilities/context, and
evaluation-backed selection.

**Done when:** selection is configurable, measured, and covered by tests; no placeholder values
remain.

## CLI and composition root

**Current:** hardcoded ticket, direct provider construction, prints text and token counts.

**Implement:** accept user input, compose dependencies, return meaningful exit codes and error
messages, and expose the same flow to tests and a future transport adapter.

**Done when:** CLI setup errors are friendly, tests cover the entry path, and no dependency is
constructed deep in application code.

## Observability

**Current:** no structured telemetry.

**Implement:** record model/provider, token usage, latency, retries, tool name/outcome, context
size, approval decision, and error class; redact secrets and sensitive content.

**Done when:** each request has a trace ID and logs pass a redaction test.

## Traceability

Supports `BR-01`, `BR-04`, `BR-08`, `BR-09`, `BR-10`, `FR-01`–`FR-15`, `NFR-05`–`NFR-14`, and
`ADR-001`–`ADR-003`.
