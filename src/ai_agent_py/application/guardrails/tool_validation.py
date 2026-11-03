from ai_agent_py.application.guardrails.errors import (
    UnsafeToolCallError,
)
from ai_agent_py.application.tools.contracts import ToolCall

ALLOWED_TOOL_NAMES = {
    "customer_lookup",
    "order_lookup",
    "business_policy_lookup",
    "refund_eligibility_assessment",
}


def validate_tool_call(call: ToolCall) -> None:
    if not isinstance(call, ToolCall):
        raise UnsafeToolCallError("Tool call has an invalid type.")

    if call.name not in ALLOWED_TOOL_NAMES:
        raise UnsafeToolCallError("Tool name is not allowlisted.")

    if not isinstance(call.arguments, dict):
        raise UnsafeToolCallError("Tool arguments must be an object.")

    if len(call.arguments) > 10:
        raise UnsafeToolCallError("Tool call contains too many arguments.")
