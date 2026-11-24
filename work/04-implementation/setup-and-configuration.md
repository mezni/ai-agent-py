# Setup and Configuration

Status: Current behavior and target design · 2026-11-24

## Prerequisites

| Requirement | Current | Notes |
| --- | --- | --- |
| Python | 3.12+ (`.python-version` is `3.12`) | Required by `pyproject.toml` |
| `uv` | Required | Used for sync, run, tests, lint |
| OpenAI API key | Required for the current CLI path | Never commit; stored in `.env` |
| OpenAI model | Required for the current CLI path | `OPENAI_MODEL` |
| Ollama runtime | Optional target | Needed only for local inference; not required for unit tests |
| SQLite | Built in | Used by `ConversationStore` |

## Commands

| Command | Purpose |
| --- | --- |
| `uv sync` | Install runtime/dev dependencies from `uv.lock` |
| `cp .env.example .env` | Create local configuration |
| `uv run ai-agent-py` | Run the current one-shot CLI |
| `uv run pytest -q` | Run full test suite |
| `uv run ruff check .` | Lint repository |
| `uv run ruff check <path>` | Lint changed files |

## Environment variables

| Variable | Current | Target | Required for |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Required by `config.py` | Required when OpenAI provider selected | Cloud provider |
| `OPENAI_MODEL` | Required by `config.py` and orchestrator/classifier | Required when OpenAI provider selected | Cloud model selection |
| `LLM_PROVIDER` | Not implemented | `openai` or `ollama` | Provider factory |
| `OLLAMA_MODEL` | Not implemented | Default target `qwen3:4b` in adapter | Local provider |
| `OLLAMA_BASE_URL` | Not implemented | Default target `http://localhost:11434` | Local provider |
| `DB_PATH` | Not implemented | Defaults to `conversations.db` | Storage location |
| `LOG_LEVEL` | Not implemented | Proposed | Observability |
| Context limits | Hardcoded in `ContextManager` | Proposed configurable | Context budgeting |
| Provider prices | Not implemented | Proposed for cost reports | Cost model |

`.env.example` currently contains only `OPENAI_API_KEY` and `OPENAI_MODEL`.

## Current configuration behavior

`src/ai_agent/config.py` calls `load_dotenv()` and reads both required variables with
`os.environ[...]`. Consequences:

- Missing values raise `KeyError` at import time, before a friendly CLI error can be shown.
- `config.py` shadows the `config/` directory, so `generation_profiles.py` and `model_catalog.py`
  cannot be imported.
- Model/provider selection is spread across `config.py`, `main.py`, `orchestrator.py`, and
  `ticket_classifier.py`.

Target behavior:

- Convert configuration into an importable package.
- Validate all settings once at startup with clear, actionable errors.
- Expose a single `Settings` object through the composition root.
- Derive secrets from environment/secret manager; never log them.
- Keep provider defaults in configuration or the factory, not in application services.

## Dependency changes

| Dependency | Current | Target action |
| --- | --- | --- |
| `openai>=3.57.0` | Declared | Keep |
| `pydantic>=2.14.4` | Declared | Keep |
| `python-dotenv>=1.2.4` | Declared | Keep |
| `pytest>=9.2.0` | Dev dependency | Keep |
| `ruff>=0.17.6` | Dev dependency | Keep |
| `ollama` | Not declared; adapter imports it | Add when local provider is enabled or make import optional with a clear error |
| Typechecker | Not configured | Proposed; add only with an agreed tool/config |
| Coverage / eval tooling | Not configured | Proposed in `../05-evaluation/` |

After changing dependencies, run `uv sync` and commit `uv.lock` together with `pyproject.toml`.

## Local setup procedure

1. `uv sync`
2. `cp .env.example .env`
3. Set `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env`.
4. Run `uv run ai-agent-py` to confirm the one-shot path.
5. Run `uv run pytest -q` and `uv run ruff check .` to record the current baseline.
6. For local inference, start Ollama separately, set its variables, and ensure the runtime API is
   restricted to trusted access.

## Security rules

- `.env` is ignored by Git; verify with `git status` before committing.
- Never print API keys, full prompts containing secrets, or sensitive customer content.
- Use environment or a secret manager; do not hardcode credentials in modules or tests.
- Test configuration uses dummy values from `tests/conftest.py`; unit tests must not call live APIs.
- Local inference is not automatically secure; restrict the Ollama API to trusted access.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `KeyError: 'OPENAI_API_KEY'` on import | Missing `.env` or variable | Copy example and set values; target should report a friendly error |
| `ModuleNotFoundError: No module named 'ollama'` | Provider imported without dependency | Add dependency or guard import |
| `cannot import name ... config` | `config.py` shadows `config/` | Complete config package migration |
| `NameError: name 'Iterator' is not defined` | Broken `OpenAIProvider.stream()` | P0/P2 fix |
| `ImportError: cannot import name 'LLMValidationError'` | Undefined error class | P0 taxonomy fix |
| Collection stops before tests run | Import-time error in a module | Fix imports first; do not skip files permanently |
| `ContextWindowExceeded` | Fixed context exceeds budget | Reduce prompt/history or raise limit within policy |
| `ToolExecutionError('Invalid tool request.')` | Unknown tool or invalid arguments | Check tool schema and argument JSON |
| Empty model output | Incomplete/refused/truncated response | Inspect response status and generation budget |

## Traceability

Supports `FR-01`, `FR-10`, `FR-14`, `FR-15`, `NFR-05`, `NFR-11`, `NFR-12`, and `ADR-001`.
