# Development Standards

## 1. General Principles

- Follow Clean Architecture.
- Keep business logic independent of frameworks.
- Prefer small, focused functions.
- Use type hints for application interfaces and domain logic.
- Avoid unnecessary abstractions.
- Make business decisions deterministic and testable.

## 2. Naming

- Modules and functions: snake_case.
- Classes: PascalCase.
- Constants: UPPER_SNAKE_CASE.
- Test functions: `test_<behavior>`.

## 3. Formatting

Use Ruff as the authoritative formatter.

```bash
uv run ruff format .
```

## 4. Linting

All lint errors must be resolved before committing.

```bash
uv run ruff check .
```

Do not disable a rule globally just to make a check pass. Document justified exceptions.

## 5. Testing

- Unit tests should isolate the behavior under test.
- Integration tests should validate interactions between components.
- Evaluation tests should use the shared evaluation datasets.
- Tests must use synthetic data.
- Tests must not depend on real customer systems.

## 6. Coverage

The initial overall coverage target is 80%.

Critical business rules must have explicit tests regardless of the overall percentage.

## 7. Type Safety

Use type annotations for public functions, domain models, and application service interfaces.

Introduce a static type checker in a later engineering step if the project needs it.

## 8. Git Workflow

Use small, focused commits.

Suggested commit format:

`<type>(ai-agent-py): <description>`

Examples:

- `feat(ai-agent-py): add ticket domain model`
- `test(ai-agent-py): add refund policy tests`
- `refactor(ai-agent-py): isolate repository adapters`

## 9. Quality Gate

Before committing:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=ai_agent_py --cov-report=term-missing
```

All checks must pass.
