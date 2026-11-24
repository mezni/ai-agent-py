# Development

Status: Local development guide · 2026-11-24

## Prerequisites

| Requirement | Version / notes |
| --- | --- |
| Python | 3.12+; `.python-version` is `3.12` |
| `uv` | Required for sync, run, tests, lint |
| OpenAI key/model | Required for the current CLI path |
| Ollama runtime | Optional; adapter exists but dependency is missing |
| SQLite | Built in; no server needed |

## First-time setup

```bash
uv sync
cp .env.example .env
```

Set `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env`. `.env` is ignored by Git; never commit real
credentials or use production keys in development/tests.

## Commands

| Command | Purpose |
| --- | --- |
| `uv sync` | Install from `uv.lock` |
| `uv run ai-agent-py` | Run the one-shot CLI |
| `uv run pytest -q` | Full suite; currently fails collection |
| `uv run pytest tests/application/test_streaming.py -q` | Focused passing suite |
| `uv run ruff check .` | Lint repository |
| `uv run ruff check <path>` | Lint changed files |
| `uv build` | Build package from `pyproject.toml` |

## Current behavior to expect

- The CLI always asks `"My order #4821 has not arrived."`; input is not configurable.
- It prints the answer plus input/output token counts.
- Tool orchestrator, conversation, and memory modules exist but are not wired into the CLI.
- Missing `OPENAI_API_KEY`/`OPENAI_MODEL` fails at import with `KeyError`.
- Full test collection fails on `Iterator` in `OpenAIProvider.stream()` and undefined
  `LLMValidationError` in `ticket_validation.py`.
- `uv run ruff check .` reports 8 errors.
- `config.py` shadows `config/`; generation profiles and model catalog cannot be imported.
- `OllamaProvider` imports `ollama`, which is not declared in `pyproject.toml`.

## Configuration

Current variables: `OPENAI_API_KEY`, `OPENAI_MODEL`.

Target variables (not all implemented): `LLM_PROVIDER`, `OLLAMA_MODEL`, `OLLAMA_BASE_URL`,
`DB_PATH`, `LOG_LEVEL`, context/turn/tool limits, generation profile, provider prices, feature
flags. See `DEPLOYMENT.md` and `../07-deployment/environment-configuration.md`.

## Project layout

```text
src/ai_agent/
├── application/     Services, ports, orchestration, conversation/memory
├── domain/          Models and validation
├── prompts/         Templates, registry, builder
├── providers/       OpenAI/Ollama adapters
├── tools/           Registry, dispatcher, schemas, mock handlers
├── config.py        Current settings module
├── config/          Profiles/model catalog (unimportable today)
└── main.py          CLI entry point
tests/               Unit tests with fakes and temp SQLite DBs
docs/SUMMARY.md      Lesson summaries
LOG.md               Development log
work/                Specs by phase
```

## Common tasks

### Run a module without live credentials

Use fakes through constructor injection. For example, pass a fake model client to
`CustomerSupportAssistant` or a temporary `ConversationStore` to `ConversationManager`. Do not mock
at the network layer when a port is available.

### Add a tool

1. Define a strict Pydantic arguments model in `tools/schemas.py`.
2. Implement a handler in `tools/`.
3. Register it in `ToolRegistry.create_registry()` as an allowlisted tool.
4. Add validation, failure, and dispatch tests.
5. ensure results are treated as untrusted data and never as instructions.

### Add a provider

1. Implement the canonical port once `ADR-004` is decided.
2. Normalize usage and errors at the adapter boundary.
3. Add shared contract tests with fakes; do not require a live runtime.
4. Add configuration/factory support and capability checks.
5. Record provider data-processing/terms approval before production use.

### Change architecture or security behavior

Read the relevant ADR/spec, update the design docs first when a boundary changes, and add tests for
the new control. See `CONTRIBUTING.md`.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `KeyError: 'OPENAI_API_KEY'` | `.env` missing or variable unset | Copy template and set value |
| Collection error `Iterator` | Broken `OpenAIProvider.stream()` | Fix import and stream implementation; see `API.md` |
| Collection error `LLMValidationError` | Undefined name in validation module | Use normalized error taxonomy |
| `ModuleNotFoundError: ollama` | Dependency not declared | Add/guard dependency; use fake in tests |
| Cannot import `config.generation_profiles` | `config.py` shadows `config/` | Convert to importable package |
| Ruff findings | Pre-existing plus new issues | Fix changed paths; baseline documented in `TESTING.md` |

## Definition of local success

A clean checkout syncs, passes lint and the full test suite, runs the CLI with dummy credentials,
and does not require a live model for unit tests. Current checkout does not yet meet this state.

## Traceability

Supports `FR-01`, `FR-10`, `FR-15`, `BR-11`, and `../04-implementation/setup-and-configuration.md`.
