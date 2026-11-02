#!/usr/bin/env bash

set -euo pipefail

echo "Running Ruff lint..."
uv run ruff check .

echo "Checking formatting..."
uv run ruff format --check .

echo "Running tests with coverage..."
uv run pytest --cov=ai_agent_py --cov-report=term-missing

echo "All quality checks passed."
