from ai_agent_py.application.tools.base import AgentTool
from ai_agent_py.application.tools.context import ToolExecutionContext
from ai_agent_py.application.tools.contracts import (
    ToolCall,
    ToolResult,
    ToolStatus,
)


class ToolRegistry:
    def __init__(self, tools: list[AgentTool]) -> None:
        self._tools = {tool.name: tool for tool in tools}

        if len(self._tools) != len(tools):
            raise ValueError("Tool names must be unique.")

    @property
    def tool_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult:
        tool = self._tools.get(call.name)

        if tool is None:
            return ToolResult(
                tool_name=call.name,
                status=ToolStatus.INVALID_ARGUMENTS,
                reason="Unknown tool.",
            )

        return tool.execute(call, context)
