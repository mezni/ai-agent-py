from ai_agent_py.application.guardrails.errors import (
    UnsafeResponseError,
)


def validate_suggested_response(response: str) -> str:
    if not isinstance(response, str):
        raise UnsafeResponseError("Suggested response must be a string.")

    normalized = response.strip()

    if not normalized:
        raise UnsafeResponseError("Suggested response must not be empty.")

    if len(normalized) > 4_000:
        raise UnsafeResponseError("Suggested response exceeds the maximum length.")

    # Prevent accidental control characters from being surfaced.
    if any(ord(char) < 32 and char not in "\n\t" for char in normalized):
        raise UnsafeResponseError("Suggested response contains invalid control characters.")

    return normalized
