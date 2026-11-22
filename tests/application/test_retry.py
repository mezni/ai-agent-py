from unittest.mock import Mock, patch

import pytest
from openai import APIConnectionError

from ai_agent.application.errors import (
    LLMNonRetryableError,
    LLMRetryExhaustedError,
)
from ai_agent.application.retry import execute_with_retry


def test_success_without_retry():
    operation = Mock(return_value="success")

    result = execute_with_retry(operation)

    assert result == "success"
    assert operation.call_count == 1


def test_retry_then_success():
    operation = Mock(
        side_effect=[
            APIConnectionError(request=None),
            "success",
        ]
    )

    with patch("ai_agent.application.retry.time.sleep"):
        result = execute_with_retry(
            operation,
            max_attempts=3,
        )

    assert result == "success"
    assert operation.call_count == 2


def test_retry_exhausted():
    operation = Mock(side_effect=APIConnectionError(request=None))

    with patch("ai_agent.application.retry.time.sleep"):
        with pytest.raises(LLMRetryExhaustedError):
            execute_with_retry(
                operation,
                max_attempts=3,
            )

    assert operation.call_count == 3


def test_non_retryable_error():
    operation = Mock(side_effect=ValueError("invalid input"))

    with pytest.raises(LLMNonRetryableError):
        execute_with_retry(operation)

    assert operation.call_count == 1
