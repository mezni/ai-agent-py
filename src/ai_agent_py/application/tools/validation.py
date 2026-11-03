from typing import Any


class ToolArgumentError(ValueError):
    pass


def require_arguments(
    arguments: dict[str, Any],
    required: set[str],
) -> None:
    if not isinstance(arguments, dict):
        raise ToolArgumentError("Arguments must be an object.")

    missing = required - arguments.keys()
    extra = arguments.keys() - required

    if missing:
        raise ToolArgumentError(f"Missing required arguments: {sorted(missing)}")

    if extra:
        raise ToolArgumentError(f"Unexpected arguments: {sorted(extra)}")


def require_non_empty_string(
    arguments: dict[str, Any],
    key: str,
) -> str:
    value = arguments.get(key)

    if not isinstance(value, str) or not value.strip():
        raise ToolArgumentError(f"'{key}' must be a non-empty string.")

    return value.strip()
