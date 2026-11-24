import random
import time
from collections.abc import Callable
from typing import TypeVar

from ai_agent.application.errors import (
    LLMRateLimitError,
    LLMTransientError,
)

T = TypeVar("T")


def calculate_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> float:
    upper_bound = min(
        max_delay,
        base_delay * (2 ** (attempt - 1)),
    )

    return random.uniform(0, upper_bound)


def execute_with_retry(
    operation: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()

        except LLMTransientError as error:
            if attempt == max_attempts:
                raise

            if (
                isinstance(error, LLMRateLimitError)
                and error.retry_after is not None
            ):
                delay = max(0.0, error.retry_after)
            else:
                delay = calculate_backoff(
                    attempt=attempt,
                    base_delay=base_delay,
                    max_delay=max_delay,
                )

            sleep(delay)

    raise RuntimeError("Unexpected retry execution state")
