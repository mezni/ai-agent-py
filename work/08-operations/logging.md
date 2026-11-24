# Logging

Status: Current gaps and target design · 2026-11-24

## Current behavior

- `src/ai_agent/main.py:13` prints the response text.
- `src/ai_agent/main.py:15-16` prints input/output token counts.
- `src/ai_agent/__init__.py:2` prints a greeting on import.
- Provider usage data is populated in `ModelResponse` by `OpenAIProvider`; it is not exported as a
  metric or structured event.
- Retry logic has no attempt-level telemetry.
- There is no logger, level, timestamp, environment, revision, trace ID, outcome field, redaction,
  sink, or retention policy.
- SDK exception text is converted to generic `RuntimeError` messages; no guarantee exists that
  future logs will not echo secret or sensitive content.

## Target format

Emit structured JSON to stdout; the platform collects it. One line per event.

| Field | Required | Notes |
| --- | --- | --- |
| `timestamp` | Yes | UTC ISO-8601 |
| `level` | Yes | `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `service` | Yes | `ai-agent-py` |
| `environment` | Yes | `dev`, `ci`, `evaluation`, `staging`, `prod` |
| `revision` | Yes | Commit SHA from build |
| `trace_id` / `span_id` | Yes for request work | Correlates logs, traces, incidents |
| `event` | Yes | Stable dot-separated name |
| `outcome` | Yes | `success`, `denied`, `failure`, `retry`, `skipped` |
| `duration_ms` | When timed | Numeric |
| `error_class` | On failure | Normalized class, not raw exception text |
| `provider` / `model` | Provider events | Approved IDs only |
| `tool_name` | Tool events | Never raw arguments/results |
| `tenant_id_hash` | Authorization events | Hash/approved identifier; no raw PII |
| `approval_decision` | Consequential actions | `approved`, `denied`, `missing` |

Example shape:

```json
{"timestamp":"2026-11-24T12:00:00Z","level":"INFO","service":"ai-agent-py","environment":"staging","revision":"abc123","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","event":"model.call.completed","outcome":"success","duration_ms":812,"provider":"openai","model":"approved-model-id","input_tokens":128,"output_tokens":74}
```

## Event catalog

| Event | Level | Key fields | Emitted by |
| --- | --- | --- | --- |
| `app.started` | INFO | revision, environment, provider, settings version | Composition root |
| `config.validated` | INFO | settings version, provider, non-secret values | Config package |
| `config.invalid` | ERROR | variable names, error_class | Config package |
| `request.accepted` | INFO | trace_id, channel, tenant hash | Transport/adapter |
| `classification.completed` | INFO | category, confidence, outcome | Classifier |
| `context.budget_applied` | DEBUG | retained/dropped counts, limits, tokens | Context manager |
| `model.call.started` | INFO | provider, model, profile, attempt | Model port/adapter |
| `model.call.completed` | INFO | duration, tokens, finish_reason, outcome | Model port/adapter |
| `retry.attempt` | WARN | operation, attempt, delay, error_class | Retry helper |
| `tool.call.started` | INFO | tool_name, allowed, tenant hash | Tool dispatcher |
| `tool.call.completed` | INFO | tool_name, outcome, duration, validation result | Tool dispatcher |
| `tool.call.denied` | WARN | tool_name, reason, tenant hash | Authorization policy |
| `approval.requested` | INFO | action, requester hash, trace_id | Approval gate |
| `approval.decision` | INFO/WARN | decision, approver role, action | Approval gate |
| `memory.access` | DEBUG | operation, key hash, owner match | Memory manager/store |
| `migration.applied` | INFO | version, name, duration, outcome | Migration runner |
| `security.denied` | WARN | control, reason, tenant hash | Security controls |
| `incident.signal` | ERROR | alert_id, runbook_id, error_class | Alert/transport bridge |

## Levels and sampling

| Level | Use |
| --- | --- |
| `DEBUG` | Development only; context budgeting, memory key hashes, detailed state transitions |
| `INFO` | Normal lifecycle, outcomes, decisions, token/cost records |
| `WARN` | Retries, denials, degraded dependency, near-budget conditions |
| `ERROR` | Terminal failure, control failure, migration failure, security signal |

Production uses `INFO` by default. `DEBUG` requires time-boxed approval and must be rechecked for
redaction before enabling. Never enable debug logging solely to inspect a customer ticket.

## Redaction rules

Never log:

- `OPENAI_API_KEY`, provider credentials, database credentials, tokens, cookies, or auth headers.
- Raw ticket text, prompt content, system prompts, model outputs, tool results, memory values,
  summaries, or retrieved documents.
- Raw exception chains from SDKs (may contain request bodies or keys).
- Raw owner IDs, customer IDs, emails, phone numbers, order details, or addresses where a hash or
  approved identifier suffices.

Allowed with validation:

- Category/enum values, counts, durations, token counts, model/tool IDs, hashes, outcomes,
  normalized error classes, approval decisions, and version identifiers.

Redaction happens before serialization, not in the log shipper. Use an allowlist field builder
rather than logging whole objects/dicts. Add a redaction test with fake secrets and fake PII.

## Storage and access

| Environment | Retention | Access | Notes |
| --- | --- | --- | --- |
| `dev` | Local only | Developer | Synthetic data only |
| `ci` / `evaluation` | Run lifetime | CI/eval owners | No raw outputs; artifacts masked |
| `staging` | Proposed 14 days | Engineering/on-call | Sanitized data |
| `prod` | Proposed 30 days; owner approval pending | Restricted on-call/security | Align with legal/retention rules |

Retention is proposed, not approved. Logs are evidence for incidents; preserve relevant entries when
an incident is open, then apply normal retention.

## Tests

- No fake secret appears in any captured log record.
- No fake PII/ticket text appears in normal or error paths.
- Every event has required fields and a stable name.
- Trace IDs propagate from request to model/tool/store/approval events.
- Error logs include normalized `error_class`, not raw exception bodies.
- `DEBUG` path is tested for redaction before any temporary enablement.
- Removal of `print()` from `main.py` and `__init__.py` verified.

## Traceability

Implements M-08, M-10, M-11, M-12, `NFR-08`, `SR-17`, and `../07-deployment/infrastructure.md`.
