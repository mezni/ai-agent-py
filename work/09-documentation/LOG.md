# Learning and Implementation Progress

Status: Condensed progress log · 2026-11-24

This file summarizes progress for handoff. The full entries remain in `../../LOG.md`; detailed lesson
notes remain in `../../docs/SUMMARY.md`. Neither is replaced here.

## Sources

| Source | Coverage |
| --- | --- |
| `../../LOG.md` | Day 1–4 and Day 70–77 entries; the later “Day 73–76” entries are a second lesson track |
| `../../docs/SUMMARY.md` | 30 lesson summaries through Lesson Day 93, including reliability/fallback/caching/observability/evaluation/guardrails/deployment |
| `work/01`–`work/09` | Requirements, architecture, design partial, implementation, security, deployment, operations, documentation specs |

## Progress timeline

| Phase | Lessons | Outcome |
| --- | --- | --- |
| Foundation | Day 1–4 | Assistant, OpenAI provider, reusable model client, prompt fundamentals |
| Prompt/tool/conversation | Day 70–76 / Summary 5–11 | Prompt versioning, structured output, parsing/errors, tool schemas/execution, conversation state, long-term memory |
| Response/model design | Lesson Day 73–77 / Summary 12–16 | Streaming, model parameters, model selection, local inference, layered architecture patterns |
| Reliability/production learning | Summary 17–30 | Error handling/retries, fallback, rate limiting, caching, cost optimization, observability, evaluation, guardrails, security engineering, testing, reliability, deployment |
| Specification work | This session | `work/01`–`work/08` packs; current `work/09` handoff pack |

## Implementation status by theme

| Theme | Status | Notes |
| --- | --- | --- |
| Customer support assistant | Partial | Working answer path; hardcoded message and token printing |
| Provider abstraction | Partial | Two incompatible contracts; no factory; stream broken; Ollama dependency missing |
| Prompts | Implemented/partial | Templates, registry, builder; classification prompt embedded in classifier/orchestrator |
| Structured output | Partial | Pydantic schema/parser; validation import broken; partial streamed JSON unsafe |
| Tools | Partial | Allowlist/strict schemas/dispatcher; mock data; unused by CLI; no approval |
| Orchestration | Partial | Exists but constructs SDK/env and embeds prompts/tools; no unit test |
| Conversation/memory | Partial | SQLite and managers exist; not wired to orchestrator; owner caller-supplied |
| Streaming | Partial/broken | Helper tests pass; provider method incomplete and breaks full collection |
| Generation/model config | Partial | Profiles/catalog exist but unimportable |
| Retries/errors | Partial | Retry helper/error taxonomy; inconsistent provider mapping |
| Fallback/caching/rate limiting/circuit breaker | Gap | Covered in lesson summaries/specs, not implemented |
| Observability | Gap | Specs only; stdout print today |
| Evaluation | Gap | Targets defined; no dataset/harness/results |
| Security controls | Gap | Threat model/specs only; no auth, approval, or redaction code |
| Deployment/CI/CD | Gap | Specs only |
| Documentation | In progress | This pack aims to make handoff reproducible |

## Key decisions and lessons

- Separate provider SDK integration from application logic with a model port and adapters.
- Parse only complete, confirmed responses; validate schema and business rules explicitly.
- Treat tool results, memory, summaries, and retrieved documents as untrusted data.
- Bound orchestration with turn/tool-call/retry limits and explicit failures.
- Use conversation history/memory as supporting context, never authoritative business state.
- Choose models/providers using measured quality, latency, cost, capability, and compliance evidence;
  README targets are not results.
- Local inference avoids per-call cloud cost but adds hardware, runtime, security, and evaluation
  responsibility.
- Architecture choices belong in ADRs; supersede rather than delete old decisions.
- Observability, cost, security, and rollback must be designed before production transition.

## Current blockers

- `Iterator` and `LLMValidationError` break full pytest collection.
- 8 Ruff findings remain.
- `ModelClient` contract conflict (`Q-12`, ADR-004 pending).
- `config.py` shadows `config/`.
- `ollama` dependency missing/unguarded.
- No evaluation evidence, auth/owner scoping, approval gate, CI/CD, migrations, or observability.

## Next steps

1. Resolve blockers and make full tests/lint green.
2. Decide and apply canonical model contract (`ADR-004`).
3. wire composition root, provider factory, and injected orchestrator dependencies.
4. Implement auth/owner scoping, approval gate, redaction, and security tests.
5. Freeze evaluation dataset/harness and measure M-01–M-12.
6. Implement migration tooling, CI/CD, and observability from the specs.
7. Keep `../../LOG.md`, `../../docs/SUMMARY.md`, ADRs, and this summary synchronized.

## Future entry convention

For each meaningful change, record: **Goal**, **Problem**, **Solution**, **Trade-offs**,
**Concepts**, **Code State**, **Evidence**, and **Next Steps**. Link ADRs/specs instead of copying
large sections.

## Traceability

Supports `BR-11`, M-15, and `../04-implementation/release-checklist.md`.
