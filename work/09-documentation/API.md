# API

Status: Current Python API · No HTTP API exists today · 2026-11-24

## API surface

`ai-agent-py` exposes a console script and importable Python modules. There is no REST/GraphQL/gRPC
service, authentication endpoint, or public webhook. The console script is:

```text
ai-agent-py = ai_agent.main:main
```

No API stability guarantee is made before version `1.0`. Treat internal module signatures as
subject to change, especially the model contract.

## Entry point

| Symbol | Signature | Behavior |
| --- | --- | --- |
| `ai_agent.main.main()` | `() -> None` | Constructs `OpenAIProvider`, runs `CustomerSupportAssistant.answer()` with a hardcoded ticket, prints response text and token counts |

Current limitation: the message is not configurable and provider construction is not injected.
See `FR-01` in `../01-discovery/functional-requirements.md`.

## Assistant API

| Symbol | Signature | Notes |
| --- | --- | --- |
| `CustomerSupportAssistant(model_client)` | constructor | Stores injected model client |
| `CustomerSupportAssistant.answer(message)` | `(str) -> ModelResponse` | Builds `ModelRequest` with support instructions and calls `model_client.generate(request)` |
| `Assistant(model_client)` | constructor | String-based helper |
| `Assistant.ask(prompt)` | `(str) -> str` | Calls `model_client.generate(prompt)` |
| `Assistant.ask_stream(prompt)` | `(str) -> Iterator[str]` | Yields chunks from `model_client.stream(prompt)` |

The two assistant classes reflect the unresolved contract conflict: `CustomerSupportAssistant`
uses `ModelRequest`/`ModelResponse`, while `ModelClient`, `Assistant`, `OllamaProvider`, and
`OpenAIProvider.stream()` use string-based generate/stream. Pending `ADR-004`.

## Model contract and providers

| Symbol | Signature | Status |
| --- | --- | --- |
| `ModelClient.generate(prompt)` | `(str) -> str` | Protocol declaration; conflicts with request/response callers |
| `ModelClient.stream(prompt)` | `(str) -> Iterator[str]` | Protocol declaration |
| `ModelRequest` | Pydantic: `message`, `instructions`, optional `model`, `max_output_tokens` | Used by `CustomerSupportAssistant` |
| `ModelResponse` | Pydantic: `text`, `model`, `input_tokens`, `output_tokens`, `total_tokens` | Returned by `OpenAIProvider.generate()` |
| `OpenAIProvider(client=None)` | constructor | Builds SDK client from settings unless injected |
| `OpenAIProvider.generate(request)` | `(ModelRequest) -> ModelResponse` | Maps SDK usage/errors; working path |
| `OpenAIProvider.stream(prompt)` | `(str) -> Iterator[str]` | Broken: missing `Iterator`, undefined `self.model`, no iteration/yields |
| `OllamaProvider(model="qwen3:4b", host="http://localhost:11434")` | constructor | Cannot import until `ollama` dependency is declared/guarded |
| `OllamaProvider.generate(prompt)` | `(str) -> str` | Local chat call |
| `OllamaProvider.stream(prompt)` | `(str)` generator | Yields non-empty chunk content |

## Classification API

| Symbol | Behavior |
| --- | --- |
| `classify_ticket(ticket: str) -> TicketClassification` | Builds prompt → calls model → parses → validates; currently constructs `OpenAI` and reads `OPENAI_MODEL` directly |
| `build_ticket_classification_prompt(ticket: str) -> str` | Template-based prompt construction |
| `PromptTemplate`, `PromptRegistry`, `create_registry()` | Versioned template storage/access |
| `parse_ticket_classification(response)` | Parses complete response into `TicketClassification`; partial/streamed JSON is invalid |
| `validate_ticket_classification(...)` | Business validation; currently broken by undefined `LLMValidationError` |
| `TicketClassification` | Pydantic result model in `domain/ticket_classification.py` |

## Conversation and memory API

| Symbol | Signature / behavior |
| --- | --- |
| `ConversationStore(db_path="conversations.db")` | Initializes SQLite schema on construction |
| `create_conversation(conversation)` | Inserts conversation |
| `add_message(conversation_id, message)` | Inserts message with FK |
| `get_messages(conversation_id, limit=None)` | Returns ordered `Message` list; rejects negative limit |
| `save_memory(conversation_id, memory)` | Upserts summary/facts |
| `get_memory(conversation_id)` | Returns `ConversationMemory` or empty |
| `save_fact(owner_id, fact)`, `get_facts(owner_id)`, `delete_fact(owner_id, key)` | Owner-scoped long-term memory operations; owner is caller-supplied today |
| `ConversationManager(store, context_manager)` | Facade over conversation operations |
| `start_conversation()`, `add_user_message()`, `add_assistant_message()`, `get_history()`, `update_memory()`, `build_context()` | Conversation workflow; no owner/auth argument today |
| `ContextManager(max_context_tokens=32000, response_reserve_tokens=4000)` | Estimates tokens, enforces budget, raises `ContextWindowExceeded` |
| `MemoryManager(store, summarizer, extractor, retriever)` | Coordinates memory |
| `process_conversation(owner_id, previous_summary, messages) -> str` | Summarizes, extracts, persists facts |
| `retrieve_relevant_memory(owner_id, query)` | Selects relevant facts |

## Tools API

| Symbol | Signature / behavior |
| --- | --- |
| `ToolDefinition`, `ToolRegistry`, `create_registry()` | Registered tools, schemas, handlers |
| `ToolDispatcher(registry).execute(tool_name, arguments)` | Validates JSON/arguments, calls handler, normalizes errors |
| `execute_tool(tool_name, arguments: str) -> str` | Legacy direct executor for `get_order_status` only |
| `get_order_status(order_id)`, `get_customer(customer_id)`, `search_faq(query)` | Mock authoritative data handlers |
| `GetOrderStatusArguments`, `GetCustomerArguments`, `SearchFAQArguments` | Strict Pydantic argument schemas |
| `ToolResult` | Normalized tool result model |

Tool calls must be allowlisted and schema-validated before handlers execute. Tool results are data,
not instructions.

## Configuration API

`ai_agent.config` exposes `settings.openai_api_key` and `settings.openai_model`, loaded from
environment/`.env` at import. Missing values raise `KeyError`. `config/generation_profiles.py` and
`config/model_catalog.py` define profiles/catalog but are currently unimportable because
`config.py` shadows the `config/` directory.

## Error model

`application/errors.py` defines `LLMError` with transient/rate-limit/timeout/connection, permanent/
authentication/invalid-request, and response-error subclasses. Inconsistent mapping remains:
`OpenAIProvider` currently raises generic `RuntimeError`, and the retry helper raises
`RuntimeError("Unexpected retry execution state")`.

## Documentation contract

Public behavior must be recorded in user docs; module signatures must match code. Changes to the
model port or provider boundary require `ADR-004` or a new ADR and updates to this file.

## Traceability

Supports `FR-01`, `FR-02`, `FR-03`, `FR-05`, `FR-06`, `FR-10`, and `Q-12`.
