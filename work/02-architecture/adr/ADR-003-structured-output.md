# ADR-003: Structured Output

## Status

Accepted · 2026-11-24

This is the agreed approach for machine-readable model results. The strict schema and parser exist,
but the validation import and streaming provider path are currently broken.

## Date

2026-11-24

## Context

Routing and tool decisions need machine-readable values such as ticket category, optional order ID,
and lookup flag. The repository already defines a strict Pydantic model with `extra="forbid"`,
`strict=True`, and a `Literal` category set (`src/ai_agent/domain/ticket_classification.py:14-22`).
`parse_ticket_classification()` checks response status, refusal content, parsed output presence,
and type (`src/ai_agent/application/response_parser.py:11-32`).

Risks to address:

- Model output can be incomplete, refused, malformed, or truncated by a small token budget.
- Partial streamed JSON is not a valid result and must never be trusted.
- Provider structured-output APIs differ, and local Ollama support must be verified.
- Free-form JSON parsing invites schema drift and silent acceptance of invalid values.
- Discovery proposes ≥99% structured-output validity but has not measured it.

## Decision

Use **provider-assisted structured output when available, followed by strict schema and business
validation of the complete response**.

1. The application requests a structured result through the canonical model port.
2. The provider adapter translates the request into provider-specific structured-output options
   and returns a complete, adapter-normalized result.
3. The application checks generation status, refusal, and completion before parsing.
4. The parsed value must conform to the strict Pydantic schema; business rules are then applied.
5. Explicit zero and `None` generation settings are handled correctly; `None` options are omitted,
   and token budgets are large enough to avoid truncation (`ADR-002`).
6. Invalid results are classified, retried when allowed, and otherwise routed to a controlled
   fallback. The application never infers a value from malformed output.
7. Partial streamed chunks are rendered to users only; they are never parsed as trusted
   classification results.
8. Schemas are versioned with prompts and included in evaluation records.

## Alternatives Considered

### Prompt for JSON and parse with string/regex extraction

- **Pros:** works with almost any text-generating model.
- **Cons:** brittle with truncation, escaped text, comments, and model drift; no strict type
  guarantee; high risk of accepting invalid values.
- **Rejected as primary:** may be an adapter-level fallback only if it preserves strict validation.

### Trust partial streamed JSON

- **Pros:** lowest perceived latency for structured results.
- **Cons:** a partial object is not a valid object; decisions could be made on incomplete or
  fabricated values.
- **Rejected:** explicit safety rule in `FR-07` and `NFR-07`.

### Schema-free dictionaries

- **Pros:** flexible, minimal code.
- **Cons:** no contract, no type guarantee, silent field drift, weak tests.
- **Rejected:** conflicts with `NFR-01` and `NFR-14`.

### Provider-specific output objects used directly by application code

- **Pros:** less translation code.
- **Cons:** vendor lock-in; hard to add Ollama or fallback; SDK types leak into domain/application.
- **Rejected:** contradicts `ADR-001` and `FR-10`.

### Prompt-only instruction without validation

- **Pros:** simplest.
- **Cons:** instruction following is not a guarantee; no measurable validity.
- **Rejected:** validation is mandatory at the trust boundary.

## Consequences

### Positive

- Downstream code receives a typed, validated value.
- Invalid, refused, and incomplete outputs produce distinguishable failures.
- Provider differences are contained in adapters.
- Evaluation can measure structured-output validity reproducibly.

### Negative

- Not every provider/model supports equivalent structured-output modes; capability checks are
  needed.
- Strict validation may reject outputs that a human would consider acceptable.
- Schema evolution requires coordination with prompts, tools, tests, and evaluation artifacts.
- Validation and retries add latency and token cost.

### Implementation obligations

1. Fix `ticket_validation.py` so its error imports resolve and errors are classified consistently.
2. Choose the canonical model contract and expose complete parsed results through it (`Q-12`).
3. Implement provider adapters that map generation/structured-output options and normalize errors.
4. Verify Ollama structured-output capability; if unavailable, provide a validated adapter fallback
   that still satisfies the strict schema.
5. Add tests for refusal, incomplete status, missing output, extra field, invalid literal, invalid
   business value, truncation, and retry exhaustion.
6. Add tests proving partial streamed JSON is never accepted as a classification result.
7. Record provider, schema version, and measured validity in evaluation reports.

### Current deviations

- `src/ai_agent/application/ticket_validation.py:1-4` imports undefined `LLMValidationError`,
  breaking collection.
- `src/ai_agent/providers/openai_provider.py:48-53` has an incomplete `stream()` method using
  undefined `Iterator` and `self.model`.
- `src/ai_agent/application/ticket_classifier.py:34-38` calls provider-specific `responses.parse`
  directly instead of going through the canonical port.
- The string-based `ModelClient` contract does not expose structured results.

## Traceability

Supports `BR-02`, `BR-04`, `BR-09`, `FR-02`, `FR-03`, `FR-07`, `FR-08`, `FR-12`, `FR-13`,
`FR-14`, `NFR-01`, `NFR-07`, `NFR-12`, `NFR-14`, and `ADR-002`.
