import pytest

from ai_agent_py.application.guardrails.errors import (
    UnsafeResponseError,
)
from ai_agent_py.application.guardrails.output_validation import (
    validate_suggested_response,
)


def test_valid_response_is_accepted():
    assert (
        validate_suggested_response("I can help check your order.")
        == "I can help check your order."
    )


@pytest.mark.parametrize(
    "response",
    ["", "  ", None, "x" * 4_001, "hello\x00world"],
)
def test_invalid_response_is_rejected(response):
    with pytest.raises(UnsafeResponseError):
        validate_suggested_response(response)
