# Environment Configuration

Status: Current and target · 2026-11-24

## Configuration sources

| Environment | Source | Secrets | Notes |
| --- | --- | --- | --- |
| Local development | `.env` from `.env.example` | Dummy or personal dev key | Never committed; prefer synthetic tickets |
| CI validation | Platform environment; `tests/conftest.py` for tests | Dummy keys only | No live provider calls in unit tests |
| Evaluation | Controlled job environment | Evaluation-scoped provider key | Frozen dataset and recorded settings |
| Staging | Platform secret store | Staging secrets | Sanitized data; same artifact as production |
| Production | Platform secret store | Production secrets | Backup and approval required |

`.env.example` currently contains only `OPENAI_API_KEY` and `OPENAI_MODEL`.

## Variables

| Variable | Type | Dev | CI | Staging/Prod | Status |
| --- | --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | Secret | Required for cloud path | Dummy in unit tests; controlled for evaluation | Secret store | Current |
| `OPENAI_MODEL` | Config | Required for cloud path | Test dummy / candidate | Approved model ID | Current |
| `LLM_PROVIDER` | Config | `openai` or `ollama` | `openai` fake | Approved provider | Target |
| `OLLAMA_MODEL` | Config | Local model ID | Not required | Approved local model if enabled | Target |
| `OLLAMA_BASE_URL` | Config | `http://localhost:11434` default | Not required | Restricted internal URL | Target |
| `DB_PATH` | Config | `conversations.db` default | Temp path in tests | Mounted volume / managed DB | Target |
| `LOG_LEVEL` | Config | `INFO` proposed | `INFO` | Approved level; no sensitive debug | Proposed |
| `MAX_CONTEXT_TOKENS` | Config | 32000 current default | Test small values | Approved limit | Partial/hardcoded |
| `RESPONSE_RESERVE_TOKENS` | Config | 4000 current default | Test small values | Approved limit | Partial/hardcoded |
| `MAX_TURNS` | Config | 5 current default | Test values | Approved limit | Partial/hardcoded |
| `MAX_TOOL_CALLS` | Config | 10 current default | Test values | Approved limit | Partial/hardcoded |
| `GENERATION_PROFILE` | Config | Task-based target | Fixed in evaluation | Approved profile | Target |
| `PROVIDER_PRICES` | Config | Not implemented | Optional report input | Approved prices for cost report | Proposed |
| `APPROVAL_REQUIRED` | Feature flag | Not implemented | Test both paths | `true` for consequential actions | Target |

## Current behavior

`src/ai_agent/config.py` calls `load_dotenv()` and reads `OPENAI_API_KEY` and `OPENAI_MODEL` with
`os.environ[...]`. Missing values raise `KeyError` at import time. Model and provider choices are
also read directly in `main.py`, `orchestrator.py`, and `ticket_classifier.py`.

Target behavior:

- one importable config package;
- one validated `Settings` object injected from the composition root;
- clear startup errors that name variables but never echo values;
- provider-specific requirements enforced by the selected provider;
- unknown or misspelled variables ignored only if non-critical; required ones fail closed;
- feature flags evaluated once, not scattered across modules.

## Provider selection matrix

| `LLM_PROVIDER` | Required variables | Optional variables | Capability checks |
| --- | --- | --- | --- |
| `openai` | `OPENAI_API_KEY`, `OPENAI_MODEL` | Generation profile, price config | Streaming, tools, structured output, context window |
| `ollama` | `OLLAMA_MODEL` | `OLLAMA_BASE_URL` | Streaming and structured output must be verified; local runtime access restricted |
| Unknown | None | — | Startup error; no fallback to default provider |

Fallback behavior requires a separate approved policy (pending ADR-005). Do not silently switch
providers with different data-processing terms.

## Target `.env.example`

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_model
LLM_PROVIDER=openai
OLLAMA_MODEL=qwen3:4b
OLLAMA_BASE_URL=http://localhost:11434
DB_PATH=conversations.db
LOG_LEVEL=INFO
```

All values are examples only. Real keys belong in a secret store in staging/production.

## Validation rules

- Required values must be non-empty; secrets must not be logged.
- `LLM_PROVIDER` must be a known registered provider.
- `DB_PATH` must point to a writable location; migrations run before application start.
- Context limits must be positive and `response_reserve_tokens < max_context_tokens`.
- Turn/tool-call limits must be non-negative, with zero meaning disabled where supported.
- Generation profiles must select a registered task name.
- Model IDs and context windows must be verified, not placeholders (`context_window=0` is invalid).

## Deployment checklist

- [ ] Correct values set for target environment and provider.
- [ ] Secrets injected from secret store, not image/source/CI output.
- [ ] Provider/model approved and capability flags verified.
- [ ] `DB_PATH` mounted and writable; backup taken before migration.
- [ ] Feature flags reviewed (approval, streaming, memory integration).
- [ ] Startup validation runs before serving requests/processing tickets.
- [ ] Config error output reviewed to ensure no values are echoed.
- [ ] Rollback configuration recorded.

## Traceability

Supports `FR-01`, `FR-10`, `FR-14`, `FR-15`, `NFR-05`, `NFR-11`, `SR-12`, and
`../04-implementation/setup-and-configuration.md`.
