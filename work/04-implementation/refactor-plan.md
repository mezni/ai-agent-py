# Refactor Plan

Status: Ordered migration from current code · 2026-11-24

## Principles

1. Make small, reversible commits; each commit leaves tests collectable.
2. Add the replacement contract/test before migrating callers.
3. Do not add new features on top of a known-broken boundary.
4. Keep behavior visible: record baseline, change, and verification for each refactor.
5. A boundary change requires an ADR; a local implementation detail does not.
6. Never silently rewrite historical decisions; supersede them.

## Refactor sequence

| ID | Refactor | Current problem | Target | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| R1 | Configuration package | `config.py` shadows `config/`; import-time `KeyError` | Importable package with validated `Settings` | Import profiles/catalog; missing-config CLI test | Restore module, keep `.env` unchanged |
| R2 | Error taxonomy | `LLMValidationError` undefined; provider/tool errors inconsistent | One classified hierarchy with sanitized messages | Full collection; error catalog tests | Revert taxonomy commit; preserve added tests where compatible |
| R3 | Canonical model contract | Two incompatible interfaces | One port chosen in `ADR-004` | Contract suite with fakes; all callers migrated | Keep shim until all callers pass |
| R4 | Provider factory/adapters | Direct SDK construction; broken stream; Ollama import fails | Factory plus contracts in adapters | Provider parity tests; no live calls in unit tests | Config flag selects old provider path temporarily |
| R5 | Orchestrator injection | Builds `OpenAI`, reads env, embeds prompts, builds registry | Injected collaborators and approval | Tool-loop, limit, denial, error tests | Feature-flag new orchestrator path |
| R6 | Conversation/memory integration | Not wired; no owner on conversations | Owner-scoped, budgeted context path | Multi-turn and isolation tests | Keep old single-turn CLI path |
| R7 | Generation/model config wiring | Profiles/catalog unimportable, placeholders | Verified catalog and profile-to-provider mapping | Builder/registry/selector tests; capability checks | Keep static model until measured |
| R8 | Observability and approval | Print-only output; no approval/audit | Structured telemetry and approval record | Redaction, trace, approval tests | Disable telemetry exporter; keep in-process logs |

## R1 — Configuration package

**Steps**

1. Create `src/ai_agent/config/__init__.py` and move settings into a module such as `settings.py`.
2. Replace `import ai_agent.config` usages with explicit imports from the package.
3. Validate required variables once; raise a friendly configuration error.
4. Keep `.env` ignored; update `.env.example` with target variables.
5. Import generation profiles and model catalog in a smoke test.

**Done when:** `uv run ai-agent-py` reports actionable errors for missing config, and both profile and
catalog modules import.

## R2 — Error taxonomy

**Steps**

1. Define `LLMValidationError` under `LLMPermanentError` or `LLMResponseError` as agreed.
2. Add tool, context, approval, and configuration errors to the catalog.
3. Map provider SDK exceptions in adapters; sanitize messages.
4. Replace broad `except Exception` in the orchestrator and dispatcher with classified handling.
5. Update `error-catalog.md` and add tests per error.

**Done when:** full pytest collection succeeds and each error has a retry decision and user outcome.

## R3 — Canonical model contract

**Current shapes**

- `ModelClient.generate(prompt: str) -> str`, `stream(prompt: str) -> Iterator[str]`
- `generate(request: ModelRequest) -> ModelResponse`

**Migration strategy**

1. Decide the target shape in `ADR-004` (`Q-12`).
2. Add a small adapter/shim around the old shape so callers can migrate incrementally.
3. Migrate one caller at a time: assistant, classifier, summarizer, orchestrator.
4. Extend the contract to represent structured results, tool calls, streaming, and usage without
   leaking SDK types.
5. Remove the shim only after all callers and tests pass on the canonical contract.

**Done when:** only one model interface remains, and provider tests exercise it with fakes.

## R4 — Provider factory and adapters

**Steps**

1. Add a factory selected from validated settings (`LLM_PROVIDER` target).
2. Implement the canonical contract in OpenAI and Ollama adapters.
3. Fix `stream()` imports, event iteration, error handling, and usage capture.
4. Map generation options centrally; omit `None`, preserve explicit zero.
5. Add capability checks before using streaming, tools, or structured output.
6. Add mocked-provider tests; no live API/runtime in unit tests.

**Done when:** both providers pass the same contract suite and capability values are verified.

## R5 — Orchestrator injection

**Steps**

1. Move prompt text into the prompt registry/builder.
2. Inject model client, tool registry/dispatcher, parser/validator, retry policy, and telemetry.
3. Keep turn/tool-call limits configurable; do not change semantics during this refactor.
4. Replace broad exception handling with classified errors.
5. Add approval gate for consequential actions.
6. Add tests for success, limits, invalid tool call, provider failure, and denied approval.

**Done when:** orchestrator contains no SDK import, environment read, or embedded prompt.

## R6 — Conversation and memory integration

**Steps**

1. Add authenticated `owner_id` to conversation creation and storage queries.
2. Extend context assembly to place long-term facts before summary and recent history.
3. Wire conversation/memory services into the orchestrator through injected collaborators.
4. Add automatic summarization triggers and stale-fact correction handling.
5. Add owner-isolation tests for read, upsert, and delete.
6. Ensure retrieved facts are labeled as untrusted supporting context.

**Done when:** a multi-turn scenario passes with fakes and no cross-owner access is possible.

## R7 — Generation and model configuration

**Steps**

1. Import profiles/catalog from the config package.
2. Replace placeholder model IDs and `context_window=0` with verified values.
3. Wire task → profile → generation options → provider mapping.
4. Wire task → model definition → provider selection through the factory.
5. Add tests for option omission, explicit zero, and unknown task/model.

**Done when:** selection is configurable and evidence-backed; no placeholder values remain.

## R8 — Observability and approval

**Steps**

1. Add trace IDs and structured events for model calls, tools, retries, context, and approvals.
2. Redact keys, tokens, and sensitive content.
3. Add an approval record object and store it with the action proposal.
4. Add alerts for error rate, latency, cost anomalies, and approval failures.
5. Verify logs with a redaction test.

**Done when:** every request can be traced without exposing secrets or customer content.

## Data migration

Current SQLite tables are `conversations`, `messages`, `conversation_memory`, and
`long_term_memories`. Adding `owner_id` to conversations/messages requires a migration:

1. Add nullable columns first, backfill deliberately, then enforce non-null in a later step.
2. Never repurpose `owner_id` from long-term memories as proof of authenticated identity without
   validating it against the auth provider.
3. Keep parameterized queries and `PRAGMA foreign_keys = ON`.
4. Add migration tests using temporary databases.
5. Preserve existing facts by key during upserts; do not delete on schema change.

## Risk controls

| Risk | Control |
| --- | --- |
| Shim becomes permanent | Track removal as a gated task with a test that fails if old interface remains |
| Config refactor breaks imports | Smoke test all `config` imports in CI |
| Provider refactor changes response semantics | Contract suite asserts text, model, usage, errors, and stream chunks |
| Multi-turn wiring leaks owner data | Owner-isolation tests before integration |
| Migration loses facts | Backfill/upsert tests on a copy of a representative database |

## Traceability

Supports `FR-02`, `FR-03`, `FR-04`, `FR-05`, `FR-06`, `FR-07`, `FR-08`, `FR-10`, `FR-12`,
`FR-14`, `FR-15`, `NFR-06`, `NFR-09`, `NFR-11`, `NFR-12`, and `ADR-001`, `ADR-002`, `ADR-003`.
