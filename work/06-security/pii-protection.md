# PII Protection

Status: Proposed controls · 2026-11-24

## PII inventory

| Data | Source | Current location | Sensitivity | Current handling |
| --- | --- | --- | --- | --- |
| Customer ticket text | User/CLI | `main.py` input, model request, conversation store | May contain names, emails, order IDs | No masking; hardcoded demo ticket today |
| Order ID / tracking number | `tools/order_tools.py`, extracted facts | Tool results, memory facts, model context | Identifier | Regex extraction in `ticket_memory_extractor.py` |
| Customer name / email | `tools/customer_tools.py` mock `CUSTOMERS` | Tool results, model context | Direct PII | Returned by `get_customer` handler |
| Conversation messages | `ConversationManager` | SQLite `messages` | Sensitive | Stored in full, no owner column |
| Conversation summary/facts | `MemoryManager` | SQLite `conversation_memory` | Sensitive | Plain text/JSON |
| Long-term facts | `TicketMemoryExtractor` | SQLite `long_term_memories` | Sensitive | Owner key, value, source, timestamps |
| Tool arguments/results | Orchestrator | In-process JSON | Sensitive/untrusted | `ToolResult.to_json()` includes raw data |
| Provider prompts/responses | `OpenAIProvider` | External provider | Sensitive | Sent via approved SDK path; no data-minimization policy yet |
| Logs/traces | Target telemetry | Not implemented | Sensitive | Must redact |
| Evaluation data | `../05-evaluation/` (not yet created) | Planned | Sensitive if real tickets | Prefer synthetic/sanitized data |
| Secrets | `.env` | Environment | Secret | Covered in `secrets-management.md` |

## Data classification

| Class | Examples | Allowed uses | Protection |
| --- | --- | --- | --- |
| Public | FAQ text, category names | Prompts, tests, docs | None beyond integrity |
| Internal | Order status, tracking number | Authorized tool responses | Access control, no public logs |
| Sensitive/PII | Names, emails, ticket text, memory | Answer generation by approved provider | Minimize, mask in logs, encrypt, retain briefly |
| Secret | API keys, provider credentials | Provider authentication only | Secret manager/env, redaction, rotation |
| Audit | Approval decisions, trace IDs | Security review | Attributed, protected, retained per policy |

## Minimize

1. Send only the current ticket, necessary tool context, and validated supporting facts to the
   provider.
2. Do not send full conversation history when a summary or selected facts suffice.
3. Do not place customer emails or names in prompts unless the task requires them.
4. Use synthetic/sanitized tickets in unit tests and the evaluation dataset unless explicitly
   approved.
5. Avoid storing raw provider responses in logs; store derived metrics and trace IDs.

## Mask and redact

| Surface | Rule |
| --- | --- |
| Application logs | Never log full ticket text, memory values, tool result data, or generated content |
| Error messages | Sanitize provider errors; no prompt echoes, keys, or customer fields |
| Traces | Record IDs, categories, tool names, outcomes, token counts, latency; redact values |
| CLI output | Show the answer intended for the user; do not print internal prompts or secrets |
| Evaluation artifacts | Mask or replace real names/emails/order IDs with synthetic values |
| Crash reports | Exclude environment, prompt bodies, and customer data unless approved |

**Current gap:** `README.md` notes CLI prints response text and token counts; no structured logging
exists yet, so no redaction test exists.

## Store and retain

Current SQLite state:

- `conversations(id, created_at)` — no owner and no deletion API.
- `messages(id, conversation_id, role, content, created_at)` — full content.
- `conversation_memory(conversation_id, summary, facts)` — JSON facts.
- `long_term_memories(id, owner_id, memory_key, memory_value, confidence, source, created_at,
  updated_at)` — upsert by owner/key and explicit `delete_fact(owner_id, key)`.

Target policy (values require owner/security approval):

| Data | Retention target | Deletion trigger |
| --- | --- | --- |
| Messages/conversation memory | Approved support retention window | Customer request, retention expiry, legal hold rules |
| Long-term facts | Shorter window; keep only useful facts | Correction, customer request, expiry |
| Logs/traces | Operational window without sensitive content | Retention expiry |
| Evaluation data | Versioned dataset lifecycle | Dataset retirement/access review |
| Backups | Same policy as source data | Expiry |

Implement deletion for conversations and memory, not just facts. Verify cascade deletes and backups.

## Provider transfer rules

- Only approved providers may receive ticket text, tool results, or memory.
- Provider terms must cover retention, residency, encryption, access, audit, and training use.
- Local Ollama avoids external transfer but still requires runtime/network protection.
- Do not send secrets, credentials, or unrelated customer records to a provider.
- Record provider/model per request for audit and incident response.

## Access and encryption

- Owner scoping derives from authenticated context (`SR-01`–`SR-03`).
- HTTPS is used for the OpenAI SDK path; local Ollama needs documented network controls.
- SQLite currently has no encryption at rest; production storage decision requires ADR-008.
- Use least-privilege file/database permissions and backups.

## Tests

- PII detector over logs/traces finds no names, emails, order IDs, or secret values.
- Provider request test asserts only allowed fields are present.
- Owner A cannot retrieve owner B's facts, messages, or summary.
- Deletion test verifies messages, memory, and facts are removed according to policy.
- Evaluation dataset lint rejects unmasked emails/phone numbers unless approved.
- Error-path test ensures SDK exceptions do not echo prompts or customer content.

## Traceability

Supports `BR-08`, `FR-05`, `FR-06`, `FR-14`, `FR-15`, `NFR-05`, `NFR-06`, `NFR-08`, `SR-10`,
`SR-13`, `SR-14`, `SR-15`, `SR-16`, `SR-21`.
