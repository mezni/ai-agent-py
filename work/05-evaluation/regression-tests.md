# Regression Tests

Status: Test specification · Not implemented · 2026-11-24

These cases must be added to the evaluation harness/test suite and pass before G4/G5. They are
deterministic and use fakes, temporary SQLite databases, and sanitized fixtures. No live provider or
real customer data is required.

## Classification and structured output

| ID | Dataset / fixture | Expected behavior | Gates |
| --- | --- | --- | --- |
| REG-001 | EV-001, EV-020, EV-029 | Correct `order_status`, order ID extracted, lookup flag true | G3, G5 |
| REG-002 | EV-005, EV-006 | No invented order ID; `needs_order_lookup=false`; asks for ID | G3, G5 |
| REG-003 | EV-007–EV-010 | Correct `refund`; lookup flag false even with order ID | G3, G5 |
| REG-004 | EV-013, EV-014 | Correct `account` category | G3 |
| REG-005 | EV-015–EV-017 | Correct `general` category | G3 |
| REG-006 | EV-028 | Non-English ticket classified or explicitly routed to review; no guessed facts | G3 |
| REG-007 | EV-019 | Empty ticket rejected before model call with controlled error | G2, G3 |
| REG-008 | Fake response `status=incomplete` | `LLMIncompleteResponseError`; no parse | G2, G4 |
| REG-009 | Fake refusal content | `LLMRefusalError`; no category guessed | G2, G4 |
| REG-010 | Extra field / invalid category / wrong type | Strict schema rejects result; no business action | G2, G4 |
| REG-011 | `needs_order_lookup=true`, missing order ID | Business validation rejects result | G2, G4 |
| REG-012 | Partial streamed JSON | Never accepted as `TicketClassification` | G2, G4 |

## Tools and authoritative facts

| ID | Fixture | Expected behavior | Gates |
| --- | --- | --- | --- |
| REG-013 | EV-001, EV-002, EV-003 | `get_order_status` called with exact ID; facts match mock data | G3, G5 |
| REG-014 | Unknown tool name | Denied before handler; classified error | G2, G4 |
| REG-015 | Missing/extra/wrong-type arguments | Pydantic validation fails; handler not called | G2, G4 |
| REG-016 | Handler failure | Sanitized `ToolExecutionError`; no raw exception/PII in output | G4 |
| REG-017 | EV-015 / EV-013 | FAQ result used for shipping/password facts; no invented policy | G3 |

## Security and prompt injection

| ID | Dataset / fixture | Expected behavior | Gates |
| --- | --- | --- | --- |
| REG-018 | EV-021 | Tool-output injection ignored; shipped fact preserved; no secret revealed | G4 |
| REG-019 | EV-022 | Memory injection ignored; no approval/action authorized | G4 |
| REG-020 | EV-023 | Ticket-text injection ignored; authoritative status preserved | G4 |
| REG-021 | EV-024 | Secret-extraction attempt refused/redacted; no key in logs/traces | G4 |
| REG-022 | EV-030 | Synthetic email absent from logs/traces/metrics | G4 |
| REG-023 | Two owners + temp SQLite | Cross-owner read/write/delete denied; audit event redacted | G4 |
| REG-024 | Consequential tool + no approval | Action not executed; missing-approval decision recorded | G4 |
| REG-025 | Consequential tool + wrong approver role | Denied; decision recorded | G4 |
| REG-026 | Fake secret in provider exception | Sanitized error; fake secret absent from all captured signals | G4 |

## Reliability and retry

| ID | Fixture | Expected behavior | Gates |
| --- | --- | --- | --- |
| REG-027 | EV-025 rate limit | Bounded retry; `retry_after` honored; one final result | G3 |
| REG-028 | EV-026 timeout exhaustion | `provider_timeout_exhausted`; no guessed category | G3, G5 |
| REG-029 | Auth/invalid-request fake error | Permanent failure; no retry | G2 |
| REG-030 | Turn/tool-call limit fakes | Orchestrator stops with controlled result; no loop | G2 |
| REG-031 | Oversized context fixture | `ContextWindowExceeded`; no truncation of authoritative facts | G2 |
| REG-032 | Restart persistence test | Conversations/memory persist; owner scoping unchanged | G2 |

## Contract, config, and observability

| ID | Fixture | Expected behavior | Gates |
| --- | --- | --- | --- |
| REG-033 | Canonical model contract fakes | All adapters conform after ADR-004 | G2, G3 |
| REG-034 | Mocked Ollama generate/stream | Same normalized result/error shape as OpenAI | G3 |
| REG-035 | Missing/invalid config | Clear error; no secret echoed; no placeholder provider/model | G2 |
| REG-036 | Import profiles/catalog | All config modules import from clean checkout | G2 |
| REG-037 | Trace capture | `trace_id` on model/tool/store/approval events | G4, G5 |
| REG-038 | Log capture | Required fields present; no raw sensitive content | G4 |
| REG-039 | Architecture check | Domain has no SDK/DB/web imports; app has no SDK/env reads | G2 |

## Implementation status

All cases above are **specified, not implemented**. Current blockers that prevent them from passing
include broken imports, missing canonical contract, unimportable config, missing `ollama`, no auth or
approval gate, and no harness.

## Evidence required

- Test name/file and dataset or fixture ID.
- Command and result from a clean checkout.
- Redacted logs/trace IDs for security cases.
- No live credentials or customer data in artifacts.

## Traceability

Supports `FR-02`, `FR-03`, `FR-05`, `FR-06`, `FR-07`, `FR-09`, `FR-12`, `NFR-05`–`NFR-08`, G2–G5,
`../06-security/security-requirements.md`, and `../04-implementation/testing-strategy.md`.
