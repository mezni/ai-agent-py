# ADR-002: LLM Classification

## Status

Accepted · 2026-11-24

This is the agreed direction for ticket classification. The current classifier demonstrates the
approach but still depends directly on the OpenAI SDK and environment.

## Date

2026-11-24

## Context

Support tickets must be classified into `order_status`, `refund`, `technical_support`, `account`,
or `general`, with an optional `order_id` and a `needs_order_lookup` flag
(`src/ai_agent/domain/ticket_classification.py:5-22`). The result drives routing and tool use, so
it must be stable, machine-readable, and measurable. Discovery proposes at least 95% accuracy and
99% structured-output validity on a representative dataset, but no dataset or measurement exists
yet (`../01-discovery/success-metrics.md`).

Constraints:

- Ticket language is varied and cannot be enumerated with a small rule set.
- Classification must work through the canonical model contract so provider/model choices can be
  changed without rewriting the workflow (`FR-02`, `FR-10`).
- Classification is a routing aid, not an authorization or business-state source.
- Generation settings should use low variation, controlled output budget, and confirmed
  completion (`README.md:157-188`).
- The existing classifier constructs `OpenAI`, reads `OPENAI_MODEL`, builds its own prompt, parses
  output, and validates it (`src/ai_agent/application/ticket_classifier.py:21-46`).

## Decision

Use an **LLM-based classifier behind the canonical model port**, with deterministic validation and
explicit failure paths.

1. The classifier sends the ticket through a versioned prompt from the prompt registry.
2. The provider/model, generation profile, and retries are injected/configured, not read from the
   environment inside the classifier.
3. The model returns a structured result conforming to `TicketClassification`.
4. The complete response is parsed and then validated against schema and business rules.
5. Low-temperature, output-bounded generation is used; response status and completion are checked
   before parsing (`ADR-003`).
6. Invalid, refused, incomplete, or retry-exhausted results are explicit failures. They are routed
   to a deterministic fallback or human review; the system never guesses a category.
7. Classification quality is measured on a versioned dataset before selecting a production model
   or profile.
8. A category alone never authorizes a consequential action or asserts business facts.

## Alternatives Considered

### Keyword and rule-based classifier

- **Pros:** deterministic, cheap, fast, easy to explain.
- **Cons:** brittle across phrasing, synonyms, typos, and mixed-language tickets; high maintenance;
  difficult to extend to new categories; no confidence semantics.
- **Rejected as primary:** may remain a fallback or pre-filter, but cannot meet varied-ticket
  accuracy expectations by itself.

### Classical ML classifier trained on labeled tickets

- **Pros:** fast inference, predictable cost, strong with enough labeled data.
- **Cons:** requires a representative labeled corpus, training/evaluation pipeline, deployment
  artifact, and retraining process; none exists today.
- **Rejected for this phase:** cost of data and operations exceeds the staged project's current
  maturity.

### Fine-tuned model

- **Pros:** can specialize on domain language and output format.
- **Cons:** high data/governance/cost requirements, version management, provider dependency, and
  no evidence yet that generic models miss the target.
- **Rejected:** revisit only if evaluation shows a persistent quality gap.

### Human-only classification

- **Pros:** highest contextual judgment.
- **Cons:** does not reduce repetitive work and cannot meet interactive latency or volume goals.
- **Rejected:** retained as the fallback for low-confidence or failed classifications.

### Ad-hoc inference inside the orchestrator

- **Pros:** fewer components.
- **Cons:** no stable schema, no isolated evaluation, repeated prompt logic, harder auditing.
- **Rejected:** contradicts `FR-02`, `FR-08`, and `FR-13`.

## Consequences

### Positive

- Handles varied natural-language tickets without enumerating rules.
- Produces a consistent schema that downstream routing and tools can rely on.
- Works with any provider that can satisfy the model contract and structured-output requirements.
- Evaluation, prompt versioning, and failure analysis are explicit.

### Negative

- Adds model latency, token cost, and non-determinism to the request path.
- Quality depends on prompt, model, generation profile, and dataset quality.
- Provider capability changes can invalidate the implementation and require re-evaluation.
- Requires a fallback/review path to avoid silent misclassification.

### Implementation obligations

1. Refactor `ticket_classifier.py` to use the canonical model port, injected prompt builder,
   injected parser/validator, and configured retry policy.
2. Remove direct `OpenAI` construction and `os.environ["OPENAI_MODEL"]` access.
3. Add tests with fake clients for success, refusal, incomplete response, malformed output,
   invalid business value, retry success, and retry exhaustion.
4. Add a versioned evaluation dataset and report accuracy, JSON validity, completion, latency,
   and token usage before production selection.
5. Record the selected model/profile and its measured results in `../01-discovery/success-metrics.md`.
6. Revisit this ADR if accuracy falls below target, new categories appear, or a simpler alternative
   wins evaluation.

### Current deviations

- `src/ai_agent/application/ticket_classifier.py:3,21-24` constructs `OpenAI`.
- `src/ai_agent/application/ticket_classifier.py:35` reads `OPENAI_MODEL` from the environment.
- The classifier uses `client.responses.parse` directly, bypassing a provider-neutral port.
- No measured accuracy or structured-output validity exists.

## Traceability

Supports `BR-02`, `BR-05`, `BR-09`, `BR-10`, `FR-02`, `FR-08`, `FR-10`, `FR-12`, `FR-13`,
`FR-15`, `NFR-01`, `NFR-04`, `NFR-09`, and `ADR-003`.
