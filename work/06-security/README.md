# Security — `ai-agent-py`

Status: Security specification · 2026-11-24

This pack defines the security and privacy design for the support agent. It builds on the trust
boundaries in `../02-architecture/system-context.md`, the authority rules in
`../03-design/domain-model.md`, and the requirements in `../01-discovery/`.

## Scope

- Application code in `src/ai_agent/**`, its configuration, and its local SQLite state.
- Data sent to and received from model providers and tool systems.
- Human approval, identity, access control, secrets, logs, and evaluation data.
- Development, CI, and local Ollama runtime practices that affect security.

Out of scope: building production authentication/authorization infrastructure, choosing a legal
compliance regime, or operating the authoritative business systems themselves.

## Documents

| File | Purpose |
| --- | --- |
| `threat-model.md` | Assets, actors, trust boundaries, threats, mitigations, residual risk |
| `security-requirements.md` | Testable `SR-xx` requirements mapped to discovery IDs |
| `prompt-injection-protection.md` | Defenses for untrusted user, tool, memory, and model text |
| `pii-protection.md` | PII inventory, minimization, masking, retention, provider transfer |
| `access-control.md` | Identity, roles, permissions, owner scoping, approval enforcement |
| `secrets-management.md` | Secret inventory, storage, rotation, redaction, CI scanning |

## Current security posture

| Area | Current control | Gap |
| --- | --- | --- |
| Secrets | `.env` ignored; dummy test values in `tests/conftest.py` | No validation, rotation, scanning, or secret manager; `.gitignore` only ignores `.env` |
| Input validation | Empty-message checks; strict Pydantic tool/classification schemas | No size limits, rate limits, or systematic user-input sanitization |
| Tool access | Allowlisted registry and strict argument schemas | No authorization, approval, auditable execution, or classified tool errors |
| Owner scoping | `long_term_memories` keyed by `(owner_id, memory_key)` with parameterized SQL | `owner_id` is caller-supplied; conversations/messages have no owner |
| Untrusted data | Orchestrator states tool results are data; memory prompt says not to follow embedded instructions | Memory is injected in a system-like context; no instruction-hierarchy tests |
| Model output | Strict schema, complete-response parse, refusal/incomplete checks | Validator import broken; no universal structured-output contract |
| Approval | Target only | No approval gate or audit record |
| Telemetry | Prints text and token counts | No structured logs, redaction, or audit events |
| Transport | OpenAI SDK over HTTPS; local Ollama HTTP target | Ollama runtime not restricted by code/config; no TLS posture documented |
| Storage | Parameterized SQL, foreign keys, cascade deletes, unique fact key | No encryption at rest, retention policy, backup, or migration layer |

## Security principles

1. **Never trust model output as authority.** Business state and permissions come from tools,
   databases, and application code.
2. **Treat all retrieved text as data.** User messages, tool results, memory, summaries, and
   provider output can contain instructions; application controls decide what executes.
3. **Derive identity from authenticated context.** Never accept `owner_id` or role from a prompt,
   tool result, or user-supplied field as authoritative.
4. **Deny by default.** Tools, actions, and data are unavailable unless explicitly allowed.
5. **Minimize sensitive data.** Collect, send, store, and log only what is needed.
6. **Fail closed.** On authorization, validation, or approval failure, do not execute.
7. **Make security testable.** Every requirement has a deterministic test with fakes, temp DBs,
   and no live credentials.

## Traceability

Uses discovery IDs `BR-08`, `BR-03`, `BR-04`, `FR-03`, `FR-05`, `FR-06`, `FR-09`, `FR-14`,
`FR-15`, `NFR-05`, `NFR-06`, `NFR-07`, `NFR-08`, `NFR-13`, and architecture decisions
`ADR-001`–`ADR-003`. New security requirements use `SR-xx`.

## Reading order

1. `threat-model.md` for what can go wrong and why it matters.
2. `security-requirements.md` for enforceable controls.
3. `prompt-injection-protection.md` for the LLM-specific attack surface.
4. `pii-protection.md` for data minimization and privacy.
5. `access-control.md` for identity, permissions, and approval.
6. `secrets-management.md` for credentials and operational hygiene.

## Change process

Update the threat model when a new trust boundary, provider, tool, data type, or transport is
added. Every new or changed control must add/update a test and a `SR-xx` entry. Changes to the
security boundary require an ADR and sign-off from the security owner.
