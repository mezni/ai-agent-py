# Secrets Management

Status: Current behavior and target controls · 2026-11-24

## Secret inventory

| Secret | Current source | Used by | Exposure risk | Target |
| --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | `.env` / environment | `config.py`, `OpenAIProvider` | Logs, errors, commits, CI artifacts | Secret manager in production; env in development; rotate |
| Provider credentials (future) | Not implemented | Provider factory/adapters | Same as above | Per-provider scoped credentials |
| Ollama API access | No credential; URL only | `OllamaProvider` | Local HTTP API exposed | Network restriction/auth proxy; treat URL as controlled config |
| Database credentials (future) | Not implemented | Target repository | Config/logs | Secret manager, least privilege |
| CI secrets | Not configured | Future evaluation/deploy jobs | Logged command output | Masked CI secrets, restricted access |
| Test dummy keys | `tests/conftest.py` | Unit tests | Mistaken for real keys | Clearly non-production values only |

`OPENAI_MODEL` and `OLLAMA_BASE_URL` are configuration, not secrets, but still require validation.

## Current controls

- `.gitignore:1` ignores `.env`.
- `.env.example` contains `OPENAI_API_KEY` and `OPENAI_MODEL`.
- `config.py` calls `load_dotenv()` then reads values with `os.environ[...]`.
- `tests/conftest.py` sets dummy `OPENAI_API_KEY=test-api-key` and `OPENAI_MODEL=test-model`.
- `OpenAIProvider` passes the key to the SDK; errors are converted to generic `RuntimeError`
  messages.

## Gaps

- Missing values fail at import with `KeyError`, before friendly CLI handling.
- `.gitignore` ignores only `.env`; variants such as `.env.local` or `.env.production` are not
  covered.
- No secret scanning in CI or pre-commit.
- No documented rotation, revocation, or incident process.
- No guarantee that future logs/traces redact secrets.
- No assertion that SDK exception text is never logged.
- No separation between development, evaluation, and production credentials.

## Target controls

### Storage

- Development: `.env` from a template, ignored by Git.
- Production/CI: secret manager or platform secret store; inject at runtime.
- Never store secrets in source, tests, docs, prompts, SQLite, evaluation artifacts, or lockfiles.
- Scope credentials per environment and provider; avoid sharing one key across all jobs.

### Handling

- Load and validate secrets once in the configuration package.
- Missing/invalid secrets produce a clear error that names the variable but never echoes its value.
- Redact secret values in logs, traces, error messages, exception chains, and CLI output.
- Keep secrets out of model requests; prompts should never contain credentials.
- Use least-privilege keys and separate keys for development, evaluation, and production.

### Git hygiene

Target `.gitignore` pattern set:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
```

Verify with `git status` before every commit and add automated secret scanning to CI.

### Rotation and revocation

| Event | Action |
| --- | --- |
| Scheduled rotation | Create new credential, update secret store, deploy, verify, revoke old key |
| Suspected exposure | Revoke immediately, search logs/artifacts, rotate, review access, record incident |
| Provider change | Remove unused credentials and update approved-provider record |
| Contributor offboarding | Revoke environment-specific access and rotate shared keys |

### Ollama runtime

- Ollama does not require an API key in the current adapter, but its HTTP API is a privileged
  local interface.
- Bind to a trusted interface, restrict with firewall/network policy, and use an auth proxy if
  accessed beyond localhost.
- Do not expose the runtime through the application transport.
- Unit tests must mock the client and never call a real runtime.

## Tests

- Secret scanner finds no credential patterns in tracked files or diffs.
- Missing configuration test reports a friendly error without echoing values.
- Log/trace redaction test injects a known fake secret and asserts absence.
- Provider error test injects SDK exception text containing a fake secret and asserts sanitization.
- `.gitignore` test confirms `.env` and `.env.*` are ignored while `.env.example` is tracked.
- Test configuration uses only dummy values and cannot reach a live provider.

## Incident response outline

1. Identify the secret, environments, and exposure window.
2. Revoke/rotate the credential first; then investigate.
3. Search repository history, CI artifacts, logs, traces, and backups.
4. Replace the secret and verify all consumers.
5. Record root cause, impact, actions, and follow-up controls.
6. Add a regression test or CI rule so the same leak is detected.

## Traceability

Supports `NFR-05`, `NFR-11`, `FR-14`, `FR-15`, `SR-10`, `SR-11`, `SR-12`, `SR-17`, and threat IDs
`T-06`, `T-11`, `T-15`.
