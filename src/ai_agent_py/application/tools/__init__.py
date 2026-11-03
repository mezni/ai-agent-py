from ai_agent_py.application.security.authorization import AuthorizationService
from ai_agent_py.application.tools.business_policy_lookup import (
    BusinessPolicyLookupTool,
)
from ai_agent_py.application.tools.customer_lookup import CustomerLookupTool
from ai_agent_py.application.tools.order_lookup import OrderLookupTool
from ai_agent_py.application.tools.refund_eligibility import (
    RefundEligibilityAssessmentTool,
)
from ai_agent_py.application.tools.registry import ToolRegistry


def build_tool_registry(
    *,
    customer_repository,
    order_repository,
    policy_repository,
    refund_policy_service,
    authorization_service: AuthorizationService | None = None,
) -> ToolRegistry:
    service = authorization_service or AuthorizationService()

    return ToolRegistry(
        [
            CustomerLookupTool(customer_repository, service),
            OrderLookupTool(order_repository, service),
            BusinessPolicyLookupTool(policy_repository, service),
            RefundEligibilityAssessmentTool(
                order_repository=order_repository,
                refund_policy_service=refund_policy_service,
                authorization_service=service,
            ),
        ]
    )
