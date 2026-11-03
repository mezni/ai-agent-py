import json
from typing import Any

from ai_agent_py.application.errors import InvalidLlmOutputError


def parse_json_object(content: str) -> dict[str, Any]:
    """Parse an LLM response that must be a JSON object."""
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise InvalidLlmOutputError("LLM response was not valid JSON.") from exc

    if not isinstance(parsed, dict):
        raise InvalidLlmOutputError("LLM response must be a JSON object.")

    return parsed


def require_string(
    payload: dict[str, Any],
    key: str,
    *,
    allow_empty: bool = False,
) -> str:
    value = payload.get(key)

    if not isinstance(value, str):
        raise InvalidLlmOutputError(f"LLM output field '{key}' must be a string.")

    if not allow_empty and not value.strip():
        raise InvalidLlmOutputError(f"LLM output field '{key}' must not be empty.")

    return value.strip()


def require_object(
    payload: dict[str, Any],
    key: str,
) -> dict[str, Any]:
    value = payload.get(key)

    if not isinstance(value, dict):
        raise InvalidLlmOutputError(f"LLM output field '{key}' must be an object.")

    return value
