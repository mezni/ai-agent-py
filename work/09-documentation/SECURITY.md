# Security

Status: Current controls, gaps, and target rules · 2026-11-24

## Trust boundaries

| Boundary | Current state | Required control |
| --- | --- | --- |
| User → application | No auth; CLI one-shot | Authenticated principal; fail closed |
| Application → model provider | OpenAI SDK with API key | Secret manager, redaction, approved data terms |
| Model → application output | Text treated as instructions in some paths | Complete, validated output only; no partial JSON |
| Tool output → model | Mock data treated as facts | Treat as untrusted data, not instructions |
| Memory/history → prompt | Injected as context | Supporting data only; owner-scoped; untrusted |
| Application → SQLite | Caller-supplied `owner_id` | Authenticated owner, scoped queries, migrations |
| Consequential action → tool | No approval gate | Recorded human approval before execution |

Threat IDs T-01–T-15 and security requirements SR-01–SR-22 are defined in `../06-security/`.

## Current controls

- `.gitignore` ignores `.env`; `.env.example` contains only placeholders.
- OpenAI errors are converted to generic `RuntimeError` messages.
- Tool registry uses an allowlist and strict Pydantic schemas; dispatcher validates arguments.
- SQLite uses parameterized SQL and `PRAGMA foreign_keys = ON`.
- Long-term memory has an owner-scoped unique key and parameterized owner queries.
- Tests use dummy credentials and do not call live providers.

## Critical gaps

- No authentication or authenticated `owner_id`.
- Conversations/messages have no owner column or owner predicates.
- No role/permission checks or approval workflow.
- No structured audit events, trace IDs, log redaction, or secret scanning.
- No migration tooling or backup policy.
- `AgentOrchestrator` still constructs OpenAI and reads environment directly.
- Prompt-injection and PII controls are specified but not implemented.

## Required rules for engineers

1. Derive identity from authenticated context; never from ticket text, tool output, model output,
   memory, or a request field.
2. Treat tool results, summaries, retrieved documents, and long-term facts as data, never as
   instructions.
3. Allow only registered tools; validate strict arguments before handler execution.
4. Require human approval for consequential actions; record decision, actor, action, and time.
5. Parse classification only after complete responses with confirmed status and schema/business
   validation.
6. Never log or export secrets, raw prompts, raw model/tool output, PII, or raw owner IDs.
7. Keep `.env` out of Git; use per-environment credentials and rotate on exposure.
8. Fail closed on missing/invalid security configuration and unknown providers/tools.

## Secrets and PII

- Secret inventory and rotation: `../06-security/secrets-management.md`.
- PII handling, minimization, retention, and deletion: `../06-security/pii-protection.md`.
- Prompt-injection defenses and test categories:
  `../06-security/prompt-injection-protection.md`.
- Access model and migration from caller-supplied owner:
  `../06-security/access-control.md`.

## Security acceptance tests

- Cross-owner read/write/delete attempts denied for conversations, messages, memory, and tools.
- Unknown and unauthorized tools denied before execution.
- Missing approval denies consequential actions.
- Tool/memory/summary prompt-injection fixtures cannot override system instructions.
- Fake secrets and fake PII absent from logs, traces, metrics, errors, and artifacts.
- Partial streamed JSON never accepted as classification output.
- Secret scanner finds no credentials in tracked files/diffs.

## Incident handling

Suspected secret exposure, owner-isolation breach, unapproved action, or data leakage is P1: revoke,
contain, preserve redacted evidence, and follow `../08-operations/incident-response.md` and
`../07-deployment/rollback-strategy.md`.

## Traceability

Supports `BR-03`, `BR-08`, `FR-06`, `FR-09`, `NFR-05`, `NFR-06`, `NFR-07`, `SR-01`–`SR-22`, and
G4 in `../01-discovery/success-metrics.md`.
