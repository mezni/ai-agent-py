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


class OrderLookupTool(AgentTool):
    name = "order_lookup"

    def __init__(self, order_repository) -> None:
        self._order_repository = order_repository

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult:
        try:
            require_arguments(call.arguments, {"order_id"})
            order_id = require_non_empty_string(
                call.arguments,
                "order_id",
            )
        except ToolArgumentError as exc:
            return ToolResult(
                self.name,
                ToolStatus.INVALID_ARGUMENTS,
                reason=str(exc),
            )

        order = self._order_repository.get_by_id(order_id)
        if order is None:
            return ToolResult(
                self.name,
                ToolStatus.NOT_FOUND,
                reason="Order not found.",
            )

        if order.customer_id != context.customer_id:
            return ToolResult(
                self.name,
                ToolStatus.DENIED,
                reason="Order is outside the authorized customer scope.",
            )

        return ToolResult(
            self.name,
            ToolStatus.SUCCESS,
            data={
                "order_id": order.id,
                "customer_id": order.customer_id,
                "status": str(order.status),
                "total": str(order.total),
            },
        )
