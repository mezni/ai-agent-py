import time
from collections.abc import Callable
from typing import TypeVar

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError,
)

from ai_agent.application.errors import (
    LLMNonRetryableError,
    LLMRetryExhaustedError,
)

T = TypeVar("T")


def is_retryable(error: Exception) -> bool:
    if isinstance(
        error,
        (
            APIConnectionError,
            APITimeoutError,
            RateLimitError,
        ),
    ):
        return True

    if isinstance(error, APIStatusError):
        return error.status_code >= 500

    return False


def execute_with_retry(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    for attempt in range(max_attempts):
        try:
            return operation()

        except Exception as error:
            if not is_retryable(error):
                raise LLMNonRetryableError(
                    "Operation failed with a non-retryable error."
                ) from error

            if attempt == max_attempts - 1:
                raise LLMRetryExhaustedError(
                    "Retry attempts exhausted."
                ) from error

            delay = base_delay * (2**attempt)
            time.sleep(delay)

    raise LLMRetryExhaustedError(
        "Operation failed unexpectedly."
    )
