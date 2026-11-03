import pytest

from ai_agent_py.application.guardrails.errors import (
    UnsafeToolCallError,
)
from ai_agent_py.application.guardrails.tool_validation import (
    validate_tool_call,
)
from ai_agent_py.application.tools.contracts import ToolCall


def test_allowlisted_tool_call_is_accepted():
    validate_tool_call(
        ToolCall(
            name="order_lookup",
            arguments={"order_id": "order-001"},
        )
    )


def test_unknown_tool_is_rejected():
    with pytest.raises(UnsafeToolCallError):
        validate_tool_call(
            ToolCall(
                name="execute_refund",
                arguments={"order_id": "order-001"},
            )
        )


def test_too_many_arguments_are_rejected():
    with pytest.raises(UnsafeToolCallError):
        validate_tool_call(
            ToolCall(
                name="order_lookup",
                arguments={f"arg_{i}": i for i in range(11)},
            )
        )


def test_non_tool_call_is_rejected():
    with pytest.raises(UnsafeToolCallError):
        validate_tool_call({"name": "order_lookup"})


def test_non_object_arguments_are_rejected():
    with pytest.raises(UnsafeToolCallError):
        validate_tool_call(
            ToolCall(
                name="order_lookup",
                arguments=["order-001"],
            )
        )
