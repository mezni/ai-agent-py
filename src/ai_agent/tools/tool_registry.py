from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel

from ai_agent.tools.customer_tools import get_customer
from ai_agent.tools.knowledge_tools import search_faq
from ai_agent.tools.order_tools import get_order_status
from ai_agent.tools.schemas import (
    GetCustomerArguments,
    GetOrderStatusArguments,
    SearchFAQArguments,
)
from ai_agent.tools.tool_schemas import TOOLS


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    schema: dict
    arguments_model: type[BaseModel]
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        if name not in self._tools:
            raise ValueError(
                f"Unsupported tool: {name}"
            )

        return self._tools[name]

    def schemas(self) -> list[dict]:
        return [
            tool.schema
            for tool in self._tools.values()
        ]

    def names(self) -> list[str]:
        return list(self._tools.keys())


def create_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="get_order_status",
            schema=TOOLS[0],
            arguments_model=GetOrderStatusArguments,
            handler=get_order_status,
        )
    )

    registry.register(
        ToolDefinition(
            name="get_customer",
            schema=TOOLS[1],
            arguments_model=GetCustomerArguments,
            handler=get_customer,
        )
    )

    registry.register(
        ToolDefinition(
            name="search_faq",
            schema=TOOLS[2],
            arguments_model=SearchFAQArguments,
            handler=search_faq,
        )
    )

    return registry
