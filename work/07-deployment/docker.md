# Docker

Status: Proposed container design · No Docker files exist today

## Current state

The project runs locally with `uv run ai-agent-py`. There is no `Dockerfile`, `.dockerignore`,
`docker-compose.yml`, image build, or container registry configuration. A container is not required
for the current one-shot CLI demo; it becomes useful when the modular monolith is exposed through a
transport adapter or needs repeatable deployment.

## Target container design

| Property | Target |
| --- | --- |
| Base | Python 3.12 slim image |
| Package manager | `uv` with locked dependencies (`uv sync --frozen`) |
| User | Non-root |
| Artifact | One image per commit SHA; no `:latest` for production |
| Secrets | Injected at runtime; never copied into the image or build args |
| State | SQLite file on a mounted volume for development/prototype; managed DB target pending ADR-008 |
| Process | One application process (`ADR-001`) |
| Providers | OpenAI over HTTPS; optional external Ollama service with restricted network |
| Health | Add a health endpoint/readiness probe only after a transport adapter exists |

## Proposed Dockerfile

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir uv
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-install-project
COPY --chown=appuser:appuser src ./src
USER appuser
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
CMD ["ai-agent-py"]
```

This is a starting point, not a merged file. It must be validated with `docker build` and adjusted
if the build backend or package metadata changes. Development tools are excluded from the runtime
image; CI runs tests outside the runtime image.

## Proposed `.dockerignore`

```gitignore
.env
.env.*
.venv/
.git/
.pytest_cache/
.ruff_cache/
__pycache__/
tests/
docs/
LOG.md
work/
```

`!.env.example` is not needed in the image. Keep the ignore list aligned with
`../06-security/secrets-management.md`.

## Proposed Compose topology

```yaml
services:
  app:
    build: .
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

For local Ollama evaluation only:

```yaml
  ollama:
    image: example/ollama-runtime
    profiles: [local-llm]
    networks:
      - internal
```

Use a real image reference approved by the platform owner when this is implemented. Do not expose
the Ollama API publicly; see `../06-security/secrets-management.md`.

## Runtime configuration

| Setting | Method | Notes |
| --- | --- | --- |
| `OPENAI_API_KEY` | Secret manager / injected environment | Never in image layers or Compose file committed to Git |
| `OPENAI_MODEL` | Environment/config | Must be an approved, verified model ID |
| `LLM_PROVIDER` | Environment/config | `openai` or `ollama` once factory exists |
| `OLLAMA_BASE_URL` | Environment/config | Restricted internal address if local provider enabled |
| `DB_PATH` | Environment/config | Point to mounted volume, e.g. `/app/data/conversations.db` |
| `LOG_LEVEL` | Environment/config | Do not enable debug logging with sensitive content |

## Build and verification commands

| Command | Purpose |
| --- | --- |
| `docker build -t ai-agent-py:<sha> .` | Build a tagged image |
| `docker run --rm --env-file .env -v <data-dir>:/app/data ai-agent-py:<sha>` | Run with injected config and durable volume |
| `docker run --rm ai-agent-py:<sha> uv run pytest -q` | Not applicable to runtime image; run tests in CI image instead |
| `docker scan` / registry scan | Proposed vulnerability scan before promotion |

Use the commit SHA as the production tag. Keep previous tags until rollback is confirmed.

## Security checklist

- [ ] No `.env`, credentials, tokens, or customer data in image layers.
- [ ] Non-root user and no unnecessary write access to application source.
- [ ] Runtime secrets injected from secret manager/masked CI secrets.
- [ ] Network egress limited to approved providers and required dependency sources.
- [ ] Ollama API restricted to trusted networks/profiles.
- [ ] SQLite volume has least-privilege permissions and backup path.
- [ ] Image scanned and base image updates reviewed.
- [ ] Health/readiness added only with a real transport endpoint.
- [ ] Container start tested with missing configuration: fails clearly, does not print secrets.

## Traceability

Supports `FR-15`, `NFR-05`, `NFR-08`, `NFR-11`, `NFR-13`, `SR-10`, `SR-11`, `SR-17`, and gates
G2/G5 in `../04-implementation/quality-gates.md`.
