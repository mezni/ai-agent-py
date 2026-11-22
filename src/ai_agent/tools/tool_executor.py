import json

from ai_agent.tools.order_tools import get_order_status
from ai_agent.tools.schemas import (
    GetOrderStatusArguments,
)


def execute_tool(
    tool_name: str,
    arguments: str,
) -> str:
    if tool_name != "get_order_status":
        raise ValueError(f"Unsupported tool: {tool_name}")

    parsed_arguments = json.loads(arguments)

    validated_arguments = GetOrderStatusArguments.model_validate(parsed_arguments)

    result = get_order_status(order_id=validated_arguments.order_id)

    return json.dumps(result)
