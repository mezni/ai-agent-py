import os

from openai import OpenAI

from ai_agent.tools.tool_executor import execute_tool
from ai_agent.tools.tool_schemas import (
    GET_ORDER_STATUS_TOOL,
)

client = OpenAI(
    timeout=30.0,
    max_retries=2,
)

TOOLS = [
    GET_ORDER_STATUS_TOOL,
]


def run_agent(user_message: str) -> str:
    response = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        instructions="""
You are a customer support assistant.

You may use tools to retrieve order information.

Rules:
- Never invent order status.
- Use get_order_status when an order ID is available
  and the user asks about order information.
- Only use information returned by the tool.
- If the order is not found, explain that.
- Do not claim a tool was executed if it was not.
""".strip(),
        input=user_message,
        tools=TOOLS,
    )

    while True:
        tool_calls = [item for item in response.output if item.type == "function_call"]

        if not tool_calls:
            return response.output_text

        tool_outputs = []

        for tool_call in tool_calls:
            result = execute_tool(
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": result,
                }
            )

        response = client.responses.create(
            model=os.environ["OPENAI_MODEL"],
            instructions="""
You are a customer support assistant.

Use tool results to answer the customer.
Do not invent information.
""".strip(),
            input=tool_outputs,
            tools=TOOLS,
        )


if __name__ == "__main__":
    answer = run_agent("Where is my order #4821?")

    print(answer)
