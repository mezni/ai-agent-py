import pytest

from ai_agent.application.errors import (
    LLMTransientError,
)
from ai_agent.application.retry import (
    execute_with_retry,
)


def test_success_without_retry():
    result = execute_with_retry(
        operation=lambda: "success",
        sleep=lambda _: None,
    )

    assert result == "success"


def test_retries_then_succeeds():
    calls = 0
    delays = []

    def operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise LLMTransientError("Temporary failure")

        return "success"

    result = execute_with_retry(
        operation=operation,
        max_attempts=3,
        sleep=delays.append,
    )

    assert result == "success"
    assert calls == 3
    assert len(delays) == 2


def test_raises_after_max_attempts():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise LLMTransientError("Provider unavailable")

    with pytest.raises(LLMTransientError):
        execute_with_retry(
            operation=operation,
            max_attempts=3,
            sleep=lambda _: None,
        )

    assert calls == 3
