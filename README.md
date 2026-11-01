# AI Agent — Plain Python

A Plain Python implementation of an AI Customer Support and Ticket Resolution Agent.

This repository is part of a portfolio comparing three approaches to building an AI agent:

- Plain Python with a custom orchestrator
- LangChain and LangGraph
- Rust with Rig and RustView

## Architecture

The application follows:

- Modular Monolith
- Clean Architecture
- Dependency Rule: source-code dependencies point inward
- Deterministic business policy enforcement
- Application-controlled tool authorization
- Human approval for sensitive recommendations

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Application language |
| uv | Dependency and environment management |
| pytest | Automated testing |
| pytest-cov | Test coverage |
| Ruff | Linting and formatting |
| Streamlit | Planned user interface |

The initial implementation uses a custom orchestrator. It does not use LangChain or LangGraph.

## Project Structure

```text
ai-agent-py/
├── app/                  # Streamlit interface
├── src/
│   └── ai_agent_py/      # Application package
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
├── docs/
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- uv

### Install

```bash
uv sync
```

### Run

```bash
uv run python -m ai_agent_py
```

### Test

```bash
uv run pytest
```

### Test with coverage

```bash
uv run pytest --cov=ai_agent_py --cov-report=term-missing
```

### Lint

```bash
uv run ruff check .
```

### Format

```bash
uv run ruff format .
```

## Scope

The initial version uses synthetic data and local fixtures.

It does not execute real financial transactions, modify real customer accounts, or autonomously issue refunds.

The LLM may propose classifications and recommendations. Deterministic application and domain logic remain authoritative for business policy decisions.

## Shared Specifications

The authoritative requirements, domain contracts, architecture decisions, guardrails, security standards, and evaluation datasets are maintained in the `ai-agent-shared` repository.

This implementation must remain consistent with those shared artifacts.

## Development Status

Repository foundation initialized. Application architecture and agent capabilities will be implemented incrementally.
