# Development Log

## Day 1 — LLM Application Architecture

### Goal
Build the foundation of a reusable LLM application.

### Problem
A direct LLM API call mixes application logic
with provider-specific implementation.

### Solution
Created an initial customer support assistant
using Python and the OpenAI SDK.

### Architecture
- Application layer
- Assistant service
- LLM provider integration

### Trade-offs
Started with a simple implementation.
Provider abstraction and prompt management
will be introduced incrementally.

### Code State
Initial LLM application implemented.

### Next Steps
- Provider-independent model client
- Prompt management
- Structured outputs


## Day 2 — LLM Provider APIs

### Goal
Understand and integrate an LLM provider API.

### Problem
The application needs reliable communication
with an external LLM provider.

### Solution
Implemented an OpenAI provider adapter
using the Responses API.

### Concepts Learned
- API authentication
- Request and response structures
- Model selection
- Token usage
- API error handling

### Trade-offs
Used the official SDK instead of implementing
raw HTTP requests.

### Code State
Provider integration implemented.

### Next Steps
- Reusable provider-independent model client
- Prompt management
- Structured outputs


## Day 3 — Reusable Model Client

### Goal
Decouple the application from LLM providers.

### Problem
The assistant was tightly coupled to OpenAI.
Provider switching and unit testing were harder.

### Solution
Introduced:
- ModelClient Protocol
- ModelRequest
- ModelResponse
- OpenAIProvider adapter
- Dependency injection

### Concepts Learned
- Abstraction
- Structural typing
- Protocol
- Dependency inversion
- Dependency injection
- Adapter pattern
- Composition root

### Trade-offs
Introduced additional abstraction and code.
Improved testing and provider flexibility.

### Code State
Provider-independent assistant implemented.

### Next Steps
- Prompt engineering
- Prompt templates
- Prompt versioning

## Day 4 — Prompt Engineering Fundamentals

### Goal
Learn to design and test effective LLM prompts.

### Problem
Generic model responses may not meet application
requirements or produce consistent outputs.

### Solution
Introduced prompt engineering:
- Role
- Task
- Context
- Constraints
- Examples
- Output specification

Separated prompt templates from application logic
and created a prompt builder.

### Concepts Learned
- Zero-shot prompting
- Few-shot prompting
- Prompt decomposition
- Prompt injection
- Prompt experimentation

### Trade-offs
Prompt complexity can improve guidance but increase
token consumption and maintenance.

### Code State
Prompt module and prompt builder implemented.

### Next Steps
- Prompt templates
- Prompt versioning
- Structured prompt management


## Day 70 — Prompt Templates and Versioning

### Component/Step
Prompt Template and Version Management

### Goal
Create reusable and versioned prompt templates.

### Problem/Friction
Prompts were hardcoded in Python, making reuse,
testing, modification, and traceability difficult.

### Solution & Trade-offs
- Created PromptTemplate abstraction.
- Introduced prompt metadata.
- Added prompt registry.
- Added ticket classification prompt v1 and v2.
- Added unit tests for rendering, registry, and prompt builder.
- Used Git for prompt version history.
- Chose Python-based templates over external prompt
  management platforms to reduce complexity.

### Active Work
LLM Engineering — Prompt Management.

### Code State
Reusable and versioned ticket classification prompts
with unit tests.

### Next Steps
Structured outputs and Pydantic validation.

## Day 71 — Structured Outputs and Pydantic

### Component/Step
LLM Structured Output Contract

### Goal
Ensure LLM output follows a predictable data structure.

### Problem/Friction
LLM free-form text is unreliable for direct consumption
by application logic and downstream services.

### Solution & Trade-offs
- Created TicketClassification Pydantic model.
- Used Literal for supported categories.
- Applied strict type validation.
- Rejected unexpected fields.
- Generated JSON Schema from Pydantic.
- Used OpenAI structured output parsing.
- Tested validation locally without API calls.
- Structured outputs improve consistency but do not
  guarantee semantic correctness.

### Active Work
LLM Engineering — Structured Outputs.

### Code State
Validated ticket classification contract with
Pydantic and structured-output experiment.

### Next Steps
Output parsing, validation failures, and recovery.


## Day 72 — Output Parsing and Error Handling

### Component/Step
LLM Response Parsing and Recovery

### Goal
Implement predictable handling of LLM response failures.

### Problem/Friction
LLM responses and provider calls can fail due to
timeouts, rate limits, refusals, incomplete responses,
parsing errors, and business validation errors.

### Solution & Trade-offs
- Introduced application-level error classes.
- Created response parser.
- Added refusal and incomplete response handling.
- Added business validation rules.
- Introduced exponential backoff retry policy.
- Classified retryable and non-retryable errors.
- Added unit tests for retry behavior.
- Integrated retry, parsing, and business validation.
- Avoided SDK retry duplication in the experiment.
- Limited retries to transient provider failures.
- Parsing and business-validation recovery remain
  controlled failure paths for future improvements.

### Active Work
LLM Engineering — Reliability.

### Code State
LLM classification pipeline with controlled retries,
response parsing, and business validation.

### Next Steps
Function calling and tool schemas.


## Day 73 — Function Calling and Tool Schemas

### Component/Step
Tool Calling and Tool Execution

### Goal
Enable the LLM to request controlled application tools.

### Problem/Friction
The LLM cannot retrieve real application data
or execute application functions without
a controlled integration.

### Solution & Trade-offs
- Implemented get_order_status tool.
- Created function tool schema.
- Introduced tool allowlist.
- Implemented tool executor.
- Validated arguments with Pydantic.
- Integrated tool calling with Responses API.
- Created tool-calling loop.
- Tested tool execution independently.
- Introduced tool security fundamentals.
- Used a mock order database for simplicity.
- Tool orchestration and execution limits remain
  areas for improvement.

### Active Work
LLM Engineering — Tool Integration.

### Code State
LLM can request an order lookup and receive
application-provided data.

### Next Steps
Tool orchestration, multiple tools,
execution limits, and control flow.


## Day 74 — Tool Execution and Orchestration

### Component/Step
Agent Tool Orchestration

### Goal
Build a reusable tool orchestration layer
for multi-tool LLM applications.

### Problem/Friction
The previous tool-calling implementation was
tightly coupled to one tool and lacked a
reusable orchestration structure.

### Solution & Trade-offs
- Introduced multiple tools.
- Created ToolRegistry.
- Implemented ToolDispatcher.
- Added Pydantic argument validation.
- Added controlled ToolResult objects.
- Introduced orchestration turn limits.
- Introduced tool-call limits.
- Preserved model output during tool continuation.
- Implemented a reusable AgentOrchestrator.
- Tested the registry and dispatcher independently.
- Used sequential orchestration for simplicity.
- Parallel execution remains a future improvement.

### Active Work
LLM Engineering — Agent Orchestration.

### Code State
Reusable multi-tool orchestration engine
with registry, dispatcher, validation,
execution limits, and error handling.

### Next Steps
Conversation state, memory, and context management.


## Day 75 — Conversation State and Context Management

### Component/Step
Conversation State, Persistence, and Token-Aware Context Assembly

### Goal
Enable the agent to handle multi-turn conversations by storing message history,
persisting conversations, and building prompts that respect token limits.

### Problem/Friction
LLM APIs are stateless, so a follow-up such as "When will it arrive?" loses the
meaning of earlier messages unless the application supplies prior context.
Unbounded history is also unsafe because it can exceed the model context window.

### Solution & Trade-offs
- Added conversation domain models with stable IDs, UTC timestamps, and content
  validation.
- Added SQLite persistence for conversations, messages, and structured memory.
- Used JSON for memory facts and cascade deletes for related rows.
- Added token estimation and a response reserve instead of a simple message cap.
- Built context from the system prompt, optional memory, recent history, and the
  current user message.
- Preserved newest history first and raised a clear error when fixed content
  cannot fit the budget.
- Kept memory as supporting context rather than authoritative business state.
- Added offline tests with temporary SQLite databases and deterministic inputs.
- Fixed packaging and test configuration so `uv run pytest -q` works directly.
- Chose a lightweight character-based token estimate; a model-specific tokenizer
  can replace it later.
- Automatic summarization of evicted history remains future work.

### Active Work
LLM Engineering — Conversation State and Context Management.

### Code State
Implemented:
- `src/ai_agent/domain/conversation.py`
- `src/ai_agent/application/conversation_store.py`
- `src/ai_agent/application/context_manager.py`
- `src/ai_agent/application/conversation_manager.py`
- `tests/application/test_conversation_store.py`
- `tests/application/test_context_manager.py`
- `tests/application/test_conversation_manager.py`

Also updated `pyproject.toml` for the `ai_agent` module, CLI entry point, and
pytest path/import settings. Documentation is recorded in `docs/SUMMARY.md`,
`README.md`, and this log.

Verification: `uv run pytest -q` reports `45 passed`. Conversation implementation
files pass Ruff; repository-wide linting retains pre-existing unrelated findings.

### Next Steps
- Integrate `ConversationManager` with `AgentOrchestrator` and the CLI.
- Run the five-turn order `#4821` support lab.
- Add automatic summarization when older messages leave the context window.
- Add conversation/user scoping and production persistence policies.


## Day 76 — Conversation Summarization and Long-Term Memory

### Component/Step
Long-Term Memory, Summarization, Fact Extraction, Retrieval, and Context Assembly

### Goal
Make stored conversation information compact, structured, owner-scoped, and retrievable so
the agent can preserve important facts without repeatedly sending full conversation history.

### Problem/Friction
Message history grows until it is expensive or exceeds the context window. Basic conversation
memory records a summary and facts, but it does not decide what is important, when to
summarize, how to retrieve relevant facts, or how to correct duplicate memories.

### Solution & Trade-offs
- Added structured `MemoryFact` records with key, value, ID, confidence, source, and
  timestamps instead of plain-text facts.
- Added `LongTermMemory` grouping by owner ID.
- Added `MemorySummarizer` and an LLM-backed implementation adapted to the existing
  `ModelClient` contract.
- Added deterministic ticket fact extraction for order ID, issue, and communication
  preference.
- Added an owner-scoped `long_term_memories` SQLite table with unique `(owner_id, memory_key)`
  and upsert behavior.
- Added keyword-based retrieval as a baseline before embeddings or vector search.
- Added `MemoryManager` to coordinate summarization, extraction, persistence, and retrieval.
- Left context assembly, automatic triggers, and orchestrator/CLI integration for later work.
- Treat stored facts and summaries as untrusted data, never as instructions.

### Active Work
LLM Engineering — Conversation Summarization and Long-Term Memory.

### Code State
Documented in `docs/SUMMARY.md` and `README.md`; the core Day 76 memory components are
implemented in six separate commits.

Implemented modules:
- `src/ai_agent/domain/memory.py`
- `src/ai_agent/application/memory_summarizer.py`
- `src/ai_agent/application/llm_memory_summarizer.py`
- `src/ai_agent/application/memory_extractor.py`
- `src/ai_agent/application/ticket_memory_extractor.py`
- `src/ai_agent/application/memory_retriever.py`
- `src/ai_agent/application/memory_manager.py`
- `src/ai_agent/application/conversation_store.py` extended with long-term memory storage

Tests:
- `tests/domain/test_memory.py`
- `tests/application/test_memory_extractor.py`
- `tests/application/test_memory_retriever.py`
- `tests/application/test_memory_manager.py`
- `tests/application/test_conversation_store.py` extended with persistence and upsert tests

There is no dedicated `tests/application/test_memory_summarizer.py`; `MemoryManager` tests use
a fake summarizer and require no live model.

Day 10 correction verified: `save_memory()` and `get_memory()` are methods on
`ConversationStore`, and `conversation_memory` is initialized before use.

Verification after implementation: `uv run pytest -q` → `52 passed`. Changed files pass Ruff;
repository-wide linting still reports pre-existing findings in unrelated modules.

### Next Steps
- Add a dedicated `LLMMemorySummarizer` test with a fake `ModelClient`.
- Connect relevant facts and updated summaries to context assembly.
- Add owner authorization and explicit owner-isolation tests.
- Add message-count or token-threshold triggers with incremental summarization.
- Run the three-conversation lab covering persistence, duplicate updates, corrections,
  clarification, and invalid extraction.
- Integrate the memory pipeline with `ConversationManager`, `AgentOrchestrator`, and the CLI.


## Day 73 — Streaming Responses

### Component/Step
Incremental Response Delivery — ModelClient, OpenAIProvider, and Assistant streaming

### Goal
Deliver LLM output incrementally so users receive generated text as it is produced.

### Prerequisite
Day 72 completed.

### Problem/Friction
Users wait for a complete LLM response before seeing any output. For support tickets this
creates unnecessary perceived latency even when useful text is already available.

### Solution
Add a `ModelClient.stream()` interface, provider-level streaming, an assistant-level
`ask_stream()` wrapper, and fake-client tests for chunk delivery and reconstruction.

### Trade-offs
Streaming improves perceived responsiveness but does not necessarily reduce total generation
time or token cost. It adds error handling, cancellation, timeout, observability, security,
logging, backpressure, and final-output validation concerns.

### Concepts
Streaming, chunks, tokens, Time to First Token (TTFT), inter-token latency, stream completion,
stream interruption, and backpressure.

### Architecture
User request → Assistant → Model Client → LLM Provider → stream chunks → client. Provider
event handling stays in `providers/`; the application depends only on the `ModelClient`
contract. The non-streaming path remains available.

### Code State
Four commits add the streaming interface, a partial `OpenAIProvider.stream()` method,
`Assistant.ask_stream()`, and `tests/application/test_streaming.py`. The provider method is
incomplete: it does not import `Iterator`, uses undefined `self.model`, and does not iterate
or yield response events. The new string-based `ModelClient` contract also conflicts with the
existing `ModelRequest`/`ModelResponse` path.

`uv run pytest tests/application/test_streaming.py -q` → `2 passed`. Full-suite collection
currently fails with `NameError: Iterator is not defined` from `openai_provider.py`.
Repository-wide Ruff reports the streaming errors plus pre-existing findings.

### Next Steps
- Import `Iterator` and complete provider event iteration and yielding.
- Handle provider error events, incomplete streams, cancellation, and provider exceptions.
- Reconcile `ModelClient` with the application's `ModelRequest`/`ModelResponse` contract.
- Wire streaming into the CLI or a transport that can flush chunks to users.
- Add TTFT, duration, and completion-status observability without logging sensitive content.


## Day 74 — Model Parameters

Stage: Stage 5, Day 74

### Component/Step
Generation Configuration and Task-Specific Parameter Profiles

### Goal
Control LLM generation behavior through explicit, task-specific parameters.

### Problem/Friction
Different tasks need different generation behavior. High temperature can make ticket
classification inconsistent, an insufficient token limit can truncate JSON, and unsupported
settings can cause provider errors or misleading experiments.

### Solution
Centralize generation settings in a frozen `GenerationConfig`, define task-specific profiles,
build provider options by omitting `None` values while preserving explicit zero values, and
integrate those options without replacing retry, error-handling, response-validation, or
streaming paths.

### Trade-offs
Centralized profiles add flexibility and reviewability but require tuning, model-compatibility
checks, repeated experiments, and ongoing maintenance. One universal configuration is simpler
but cannot balance consistency, creativity, output length, and cost across tasks.

### Concepts
Temperature, top-p, maximum output tokens, frequency penalty, presence penalty, stop
sequences, nucleus sampling, output truncation, completion status, and aggregate evaluation.

### Architecture
Application request → task type → generation profile → `GenerationConfig` → provider options →
LLM → output validation. The application chooses the task profile; the provider translates it
into model-specific parameters.

### Code State
Local commits add a frozen `GenerationConfig`, `build_generation_options()`, classification,
extraction, customer-response, and RAG profiles, plus three offline builder tests. Those tests
report `3 passed`. The builder drops `None` values while preserving explicit `0.0` values.

The profile module is currently at `src/ai_agent/config/generation_profiles.py`, but importing
it fails because `src/ai_agent/config.py` resolves as a module and `src/ai_agent/config/` is not
a package. The profiles are therefore not usable from the application yet. `ModelRequest`
still exposes only `max_output_tokens`, and `OpenAIProvider.generate()` already sends that
value.

The full suite remains blocked by the separate streaming-provider `Iterator` import error.
Streaming-specific tests still report `2 passed`.

### Next Steps
- Move the profiles to `src/ai_agent/generation_profiles.py` or convert `config` into a package.
- Check each selected parameter against the target model/API before provider integration.
- Integrate profiles with the existing `ModelRequest`/provider path without duplicating retry
  or error handling.
- Run repeated experiments over a representative dataset and record `experiments/model-parameters.md`.


## Day 75 — Model Selection

Stage: Stage 5, Day 75

### Component/Step
Model Registry, Task-Based Selection, and Evaluation Matrix

### Goal
Select appropriate LLMs for different application tasks.

### Problem/Friction
One model may be too expensive, slow, or unsuitable for every task. Classification, complex
reasoning, customer responses, RAG, and sensitive enterprise workloads have different quality,
latency, capability, deployment, and compliance requirements.

### Solution
Define measurable requirements, compare candidates on a representative dataset, evaluate cost,
latency, quality, capabilities, reliability, deployment, and compliance, then centralize verified
model definitions in a registry with a deterministic task-based selection policy.

### Trade-offs
Multi-model flexibility can improve quality and cost but adds routing complexity, evaluation
work, provider variance, fallback requirements, and operational overhead.

### Concepts
Model quality, TTFT, TTLT, inter-token and end-to-end latency, token-based cost estimation,
context-window budgeting, model capabilities, provider reliability, cloud/self-hosted/hybrid
deployment, security/compliance gates, model registry, task selector, routing, and continuous
re-evaluation.

### Architecture
Application task → `ModelSelector` → `ModelRegistry` → verified `ModelDefinition` → provider
model. Production routing can add capability validation, cost limits, availability checks,
fallback, and observability.

### Code State
Local commits add `ModelDefinition`, `ModelRegistry`, `ModelSelector`,
`src/ai_agent/config/model_catalog.py`, and registry/selection tests. The six targeted tests
report `6 passed`. Selection is not wired into the application, and
`experiments/model-selection.md` does not exist yet.

The catalog still uses placeholder model IDs and `context_window=0`. It is not importable because
`src/ai_agent/config.py` is a module and `src/ai_agent/config/` has no `__init__.py`.

### Next Steps
- Move the catalog to an importable location or convert `config` into a package.
- Register reviewed candidate models, replacing all placeholder IDs and unknown context values.
- Wire verified capability and context-window checks into selection.
- Build `experiments/model-selection.md` from repeated evaluations on the shared ticket dataset.
- Document the final model choice, rejected alternatives, limitations, and fallback strategy.


## Day 76 — Local LLM Inference

Stage: Stage 5, Day 76

### Component/Step
Ollama Runtime, Local Provider, and Provider Factory

### Goal
Run and integrate local LLM inference.

### Problem/Friction
Dependence on cloud APIs, external processing and usage-based inference.

### Solution
Use Ollama to run a local model, add an `OllamaProvider` behind the shared `ModelClient`
interface, select providers through configuration and a factory, and compare local and cloud
inference on the same ticket dataset.

### Trade-offs
More control and potentially lower inference costs versus hardware, performance and maintenance requirements.

### Concepts
Local inference, hardware and runtimes, GGUF, quantization, KV-cache memory overhead, Ollama CLI
and HTTP API, provider abstraction, configuration-based factories, mocked provider tests, cloud/
local evaluation, runtime security, and local scaling/monitoring responsibilities.

### Architecture
Ticket → AI agent → `ModelClient` → provider factory → OpenAI provider or `OllamaProvider` →
cloud LLM or Ollama runtime → local model → response validation → human approval for
consequential actions.

### Code State
Documentation-only update. No Ollama dependency, `OllamaProvider`, provider factory, mocked
provider tests, or local-inference experiment files exist yet.

The current `ModelClient` is string-based, while the rest of the application still uses
`ModelRequest`/`ModelResponse`. The full suite remains blocked by the separate
`OpenAIProvider.stream()` `Iterator` import error.

### Next Steps
- Add the Ollama dependency and verify `ollama --version`, `ollama pull`, and `ollama list`.
- Implement `OllamaProvider.generate()` and a yielding `stream()` behind the shared interface.
- Reconcile `ModelClient` with the application's request/response contract.
- Add `LLM_PROVIDER`, `OLLAMA_MODEL`, and `OLLAMA_BASE_URL` configuration and a provider factory.
- Add mocked provider tests, keeping `.env` and API keys out of Git.
- Build `experiments/local-inference-dataset.json` and compare cloud/local quality, latency,
  token usage, resources, and capabilities.
- Restrict the Ollama API to trusted access and document local runtime monitoring and updates.
