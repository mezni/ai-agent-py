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


class CustomerLookupTool(AgentTool):
    name = "customer_lookup"

    def __init__(self, customer_repository) -> None:
        self._customer_repository = customer_repository

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult:
        try:
            require_arguments(call.arguments, {"customer_id"})
            customer_id = require_non_empty_string(
                call.arguments,
                "customer_id",
            )
        except ToolArgumentError as exc:
            return ToolResult(
                self.name,
                ToolStatus.INVALID_ARGUMENTS,
                reason=str(exc),
            )

        if customer_id != context.customer_id:
            return ToolResult(
                self.name,
                ToolStatus.DENIED,
                reason="Customer scope mismatch.",
            )

        customer = self._customer_repository.get_by_id(customer_id)
        if customer is None:
            return ToolResult(
                self.name,
                ToolStatus.NOT_FOUND,
                reason="Customer not found.",
            )

        # Return only the minimum fields needed by the agent.
        return ToolResult(
            self.name,
            ToolStatus.SUCCESS,
            data={
                "customer_id": customer.id,
                "display_name": getattr(customer, "name", None),
                "tier": getattr(customer, "tier", None),
            },
        )
