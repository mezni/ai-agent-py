# Security Requirements

Status: Proposed · 2026-11-24

`SR-xx` requirements are testable controls. **Current** describes the checkout; **Target** is the
required state before release.

| ID | Requirement | Priority | Traces | Current | Target |
| --- | --- | --- | --- | --- | --- |
| SR-01 | Derive `owner_id` from authenticated context | Critical | `FR-05`, `FR-06`, `NFR-06` | Caller-supplied | Authenticated principal only |
| SR-02 | Scope conversations, messages, memory, and tools to the authenticated owner | Critical | `FR-05`, `FR-06`, `FR-14` | Facts scoped; conversations not | All owner-scoped |
| SR-03 | Reject cross-owner read/write/delete attempts | Critical | `NFR-06` | Untested | 0 violations in tests |
| SR-04 | Allow only registered tools with validated strict arguments | High | `FR-03`, `ADR-001` | Observed | Preserved + audited |
| SR-05 | Deny tool execution without authorization and required permissions | Critical | `FR-03`, `FR-14` | Missing | Deny by default |
| SR-06 | Require recorded human approval before consequential actions | Critical | `FR-09`, `NFR-06` | Missing | Mandatory gate |
| SR-07 | Treat user text, tool results, memory, summaries, and model output as data | High | `FR-03`, `FR-06`, `FR-14` | Partly stated in prompts | Enforced in code and tests |
| SR-08 | Validate every structured model result against schema and business rules | High | `FR-02`, `ADR-003` | Parser exists; validator broken | Complete path green |
| SR-09 | Never accept partial streamed JSON as a trusted result | High | `FR-07` | Rule stated; stream broken | Tested |
| SR-10 | Redact secrets and sensitive content from logs, errors, and traces | High | `FR-15`, `NFR-05` | Not implemented | Tested redaction |
| SR-11 | Never commit secrets; scan diffs and repository in CI | High | `NFR-05` | `.env` ignored; no scanning | Secret scanning green |
| SR-12 | Validate configuration at startup with actionable errors | Medium | `FR-15`, `NFR-11` | Import-time `KeyError` | Friendly validation |
| SR-13 | Use approved providers under approved data terms | High | `FR-10`, `NFR-08` | Not enforced | Provider approval recorded |
| SR-14 | Minimize and mask PII in prompts, storage, logs, and evaluation data | High | `NFR-08` | Not defined | Policy + tests |
| SR-15 | Define and enforce retention/deletion for conversations, memory, logs, and datasets | High | `NFR-08` | Fact delete only | Full policy + tests |
| SR-16 | Encrypt sensitive data in transit and at rest where required | High | `NFR-08` | HTTPS via SDK; SQLite unencrypted | Approved controls |
| SR-17 | Restrict local Ollama runtime access | High if enabled | `NFR-05` | Not documented | Network + config controls |
| SR-18 | Bound request cost, turns, tool calls, retries, and context size | Medium | `NFR-02`, `NFR-07` | Partial | Configured + tested |
| SR-19 | Maintain an audit trail for tool calls, approvals, and security decisions | Medium | `FR-15` | Missing | Required fields recorded |
| SR-20 | Keep dependency lockfile current and review new dependencies | Medium | `NFR-11`, `NFR-12` | `uv.lock` present | CI dependency check |
| SR-21 | Segment and protect evaluation datasets | Medium | `BR-09`, `FR-13` | Not created | Synthetic/sanitized + access control |
| SR-22 | Verify security controls with deterministic tests before release | Critical | `BR-09`, `FR-15` | Missing | G4 green |

## Detailed requirements

### SR-01 / SR-02 / SR-03 — Identity and isolation

**Acceptance:** every conversation, message, memory fact, and tool call is associated with an
authenticated principal; a test with a mismatched owner receives a denial and no data. No code path
accepts `owner_id` from user text, model output, tool results, or unvalidated request fields.

### SR-04 / SR-05 / SR-06 — Tool and action control

**Acceptance:** registry rejects unknown tools; strict schemas reject extra/invalid arguments;
handlers are never called on validation failure; consequential actions require an approval record
with approver, action, arguments, timestamp, and decision; denial blocks execution.

### SR-07 / SR-08 / SR-09 — Untrusted data and output

**Acceptance:** tests include instruction-like content in user text, tool results, memory, and
summaries; none changes system rules or causes an unapproved tool call. Only complete responses are
parsed, validated, and used. Partial streamed JSON is rejected.

### SR-10 / SR-11 / SR-12 — Secrets and configuration

**Acceptance:** a secret placed in provider errors, prompts, logs, or traces is redacted; CI secret
scanning passes; missing configuration yields a clear error that does not echo values; `.env` and
related local files are ignored while `.env.example` remains tracked.

### SR-13 / SR-14 / SR-15 / SR-16 — Privacy and provider handling

**Acceptance:** approved provider recorded; only necessary ticket fields are sent; PII in logs and
evaluation artifacts is masked; retention/deletion rules exist for each store; transport and
storage controls match the approved policy.

### SR-17 — Local runtime

**Acceptance:** Ollama is bound to trusted interfaces, protected by network controls/proxy, and
documented; unit tests never require the runtime.

### SR-18 — Resource abuse

**Acceptance:** configurable turn/tool-call/token/retry limits; timeouts; bounded buffers; tests for
loop limit, context overflow, and retry exhaustion.

### SR-19 — Audit

**Acceptance:** each model call, tool call, approval decision, and security denial has a trace ID
and required fields without sensitive content.

### SR-20 / SR-21 / SR-22 — Supply chain, data, verification

**Acceptance:** dependency changes reviewed and locked; evaluation data synthetic or sanitized and
access-controlled; G4 safety tests pass from a clean checkout.

## Traceability

Supports `BR-03`, `BR-04`, `BR-08`, `BR-09`, `FR-02`, `FR-03`, `FR-05`, `FR-06`, `FR-07`,
`FR-09`, `FR-13`, `FR-14`, `FR-15`, `NFR-02`, `NFR-05`, `NFR-06`, `NFR-07`, `NFR-08`, `NFR-11`,
`NFR-12`, `NFR-13`, and gates G4/G5 in `../01-discovery/success-metrics.md`.
