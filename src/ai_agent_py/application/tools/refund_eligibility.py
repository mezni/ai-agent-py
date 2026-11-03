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


class RefundEligibilityAssessmentTool(AgentTool):
    name = "refund_eligibility_assessment"

    def __init__(
        self,
        *,
        order_repository,
        refund_policy_service,
    ) -> None:
        self._order_repository = order_repository
        self._refund_policy_service = refund_policy_service

    def execute(
        self,
        call: ToolCall,
        context: ToolExecutionContext,
    ) -> ToolResult:
        try:
            require_arguments(call.arguments, {"order_id", "reason"})
            order_id = require_non_empty_string(
                call.arguments,
                "order_id",
            )
            reason = require_non_empty_string(
                call.arguments,
                "reason",
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

        assessment = self._refund_policy_service.assess(
            order=order,
            requested_amount=order.total,
            reason=reason,
            image_verification_status=None,
        )

        # Serialize an explicit, bounded policy result.
        return ToolResult(
            self.name,
            ToolStatus.SUCCESS,
            data={
                "order_id": order.id,
                "eligibility": str(assessment.eligibility),
                "amount": str(getattr(assessment, "approved_amount", "")),
                "policy_version": getattr(
                    assessment,
                    "policy_version",
                    "1.0.0",
                ),
                "reasons": list(getattr(assessment, "reasons", ())),
            },
        )
