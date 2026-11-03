from typing import Protocol

from ai_agent_py.application.tools.context import ToolExecutionContext
from ai_agent_py.application.tools.contracts import ToolCall, ToolResult


class AgentTool(Protocol):
    @property
    def name(self) -> str: ...

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult: ...
