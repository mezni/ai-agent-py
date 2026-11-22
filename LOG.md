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
