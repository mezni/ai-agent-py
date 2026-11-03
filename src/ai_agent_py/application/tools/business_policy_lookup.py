from ai_agent_py.application.tools.base import AgentTool
from ai_agent_py.application.tools.context import ToolExecutionContext
from ai_agent_py.application.tools.contracts import (
    ToolCall,
    ToolResult,
    ToolStatus,
)
from ai_agent_py.application.tools.validation import (
    ToolArgumentError,
    require_arguments,
    require_non_empty_string,
)


class BusinessPolicyLookupTool(AgentTool):
    name = "business_policy_lookup"

    def __init__(self, policy_repository) -> None:
        self._policy_repository = policy_repository

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult:
        try:
            require_arguments(call.arguments, {"policy_type"})
            policy_type = require_non_empty_string(
                call.arguments,
                "policy_type",
            )
        except ToolArgumentError as exc:
            return ToolResult(
                self.name,
                ToolStatus.INVALID_ARGUMENTS,
                reason=str(exc),
            )

        policy = self._policy_repository.get_by_type(policy_type)
        if policy is None:
            return ToolResult(
                self.name,
                ToolStatus.NOT_FOUND,
                reason="Policy not found.",
            )

        return ToolResult(
            self.name,
            ToolStatus.SUCCESS,
            data={
                "policy_type": policy_type,
                "policy_version": policy.version,
                "content": policy.content,
            },
        )
