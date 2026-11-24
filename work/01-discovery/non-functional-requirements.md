# Non-Functional Requirements

Status: Proposed · 2026-11-24

Targets below are proposals derived from repository guidance unless marked **Observed**. None of
the model-quality or latency targets has been measured yet.

| ID | Category | Requirement / target | Measurement | Status |
| --- | --- | --- | --- | --- |
| NFR-01 | Quality | ≥95% classification accuracy and ≥99% structured-output validity on the agreed dataset | Versioned evaluation report | Proposed, unmeasured |
| NFR-02 | Performance | Average end-to-end response latency <2 s under agreed load; P95 agreed with owner | Instrumented traces | Proposed, unmeasured |
| NFR-03 | Streaming | TTFT, completion, and inter-token latency recorded; bounded buffers prevent unbounded growth | Streaming load test | Planned |
| NFR-04 | Cost | Per-ticket and monthly cost within approved budget, including retries and infrastructure | Token/usage + infrastructure report | Proposed, unmeasured |
| NFR-05 | Security | Secrets never committed or logged; provider/data terms approved before production | Secret scan, log audit, approval record | Partial |
| NFR-06 | Authorization | Owner IDs from authenticated context; no cross-owner access; consequential actions gated | Owner-isolation and approval tests | Partial/planned |
| NFR-07 | Reliability | Provider/tool failures degrade safely; retries bounded; no partial JSON trusted | Failure-injection tests | Partial |
| NFR-08 | Data handling | Conversation/memory retention, residency, encryption, and redaction follow agreed policy | Policy review + storage audit | Planned |
| NFR-09 | Maintainability | Domain has no provider/SDK/DB dependency; all layers use one canonical model contract | Architecture review + import checks | Partial |
| NFR-10 | Documentation | README, specs, ADRs, and known gotchas are current with significant changes | Review checklist | Partial |
| NFR-11 | Portability | Python 3.12+, `uv`-managed dependencies, reproducible lockfile; local and cloud runnable | Clean-environment setup | Observed/partial |
| NFR-12 | Testability | Unit tests use fakes and temp DBs; full suite and Ruff pass on every change | `uv run pytest -q`, `uv run ruff check .` | Failing at baseline |
| NFR-13 | Observability | Structured logs, metrics, and traces for model calls, tools, retries, context, and approvals | Dashboard/alert review | Planned |
| NFR-14 | Compatibility | Unsupported provider parameters omitted; explicit zero values preserved; context fits prompt + history + tools + reserve | Contract and context tests | Partial |

## Detailed requirements

### NFR-01 — Model quality

Classification must meet the agreed accuracy and structured-output validity thresholds before the
agent is used for automated support. Invalid, refused, or incomplete output must be counted as a
failure, not silently repaired by assuming a category. Token budgets must be large enough to avoid
truncating JSON. Thresholds are proposed in `README.md:208-210` and must be confirmed with the
product owner.

### NFR-02 — Latency

Interactive responses should average under 2 seconds at expected volume, with a P95 target agreed
during discovery. Measurement must separate TTFT, TTLT, inter-token latency, tool time, retry
time, and end-to-end time. Local inference comparisons must use the same dataset and report P95
alongside the average.

### NFR-03 — Streaming behavior

Streaming improves perceived responsiveness, not necessarily total generation time or cost. The
implementation must support cancellation, connection/read timeouts, bounded buffers for
backpressure, sanitized error messages, and logs that avoid sensitive generated content. The
complete response is validated before any structured use.

### NFR-04 — Cost

Cost estimation follows `(input_tokens / 1,000,000) × input_price + (output_tokens / 1,000,000) ×
output_price`, extended with cached input, retries, and infrastructure. The illustrative case of
10,000 tickets/day, 1,000 input tokens, and 300 output tokens at $2/$8 per million is about
$44/day or $1,320 per 30 days before retries, caching, and infrastructure
(`README.md:212-215`). It is a model, not an observation.

### NFR-05 — Security of credentials and data

`.env` is ignored and must never contain committed secrets. API keys, Ollama runtime access,
stored data, and generated logs require defined controls. Local inference is not automatically
secure; the Ollama API must be restricted to trusted access. Provider selection requires security
and compliance approval covering retention, residency, encryption, access, audit, and data terms.

### NFR-06 — Identity, authorization, and approval

`owner_id` must come from authenticated application context, not a caller-supplied free-form
value. Conversation, memory, and tool access must be scoped to that identity. Retrieved memories
and tool results are untrusted data. Consequential actions require an explicit, recorded human
approval before execution.

### NFR-07 — Reliability and failure semantics

Distinguish transient, non-retryable, validation, authorization, and tool errors. Use bounded
retry with jitter/backoff and a single consistent policy across the classifier, providers, and
orchestrator. Timeouts, rate limits, invalid output, context overflow, and tool failures must
produce controlled results. SDK-level and application-level retry settings must not conflict.

### NFR-08 — Privacy and retention

Define retention periods and deletion behavior for conversations, messages, summaries, facts,
logs, and evaluation data. Apply encryption at rest and in transit where required, redact
sensitive content in telemetry, and honor the approved provider data-processing terms. Current
SQLite storage has parameterized queries and cascade deletes but no production retention policy.

### NFR-09 — Architecture boundaries

The domain layer must not depend on OpenAI, Ollama, FastAPI, SQLite, or other infrastructure.
High-level workflow code depends on the `ModelClient` abstraction; provider adapters own SDK and
HTTP details. A single contract must replace the current string-based and
`ModelRequest`/`ModelResponse` interfaces. Configuration lives in an importable package.

### NFR-10 — Documentation and decision records

The README covers quick start, commands, and architecture. Significant choices (canonical
contract, provider strategy, storage, approval flow, evaluation) need ADRs under
`docs/decisions/` with status, context, decision, alternatives, and consequences. Specs must be
updated when behavior changes.

### NFR-11 — Environment and reproducibility

Python 3.12+, `uv sync`, locked dependencies, and the documented commands are the baseline. The
missing `ollama` dependency must be added when the local provider is enabled. Configuration must
fail clearly when required values are absent or misspelled.

### NFR-12 — Quality gates

Full test collection currently fails because `OpenAIProvider.stream()` references an unimported
`Iterator` and `ticket_validation.py` imports an undefined `LLMValidationError`. Ruff reports 8
errors at baseline. Before release, tests and lint must pass, and a static typechecker or
equivalent contract check should be adopted.

### NFR-13 — Observability

Record structured metrics for provider calls, model ID, token usage, latency, retries, tool name
and outcome, context size, memory retrieval, approval decisions, and error class. Logs must not
include secrets or sensitive generated content. Alerts should cover elevated error rates,
latency regressions, cost anomalies, and approval failures.

### NFR-14 — Provider compatibility

Translate task profiles into provider options centrally. Omit unsupported `None` values, preserve
explicit `0.0`, verify response completion before parsing, and confirm model capabilities and
context limits from provider documentation. Fixed prompts, history, tools, retrieved facts, and
reserved output must fit the context budget; otherwise the system fails explicitly.
