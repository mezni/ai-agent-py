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
) -> ToolRegistry:
    return ToolRegistry(
        [
            CustomerLookupTool(customer_repository),
            OrderLookupTool(order_repository),
            BusinessPolicyLookupTool(policy_repository),
            RefundEligibilityAssessmentTool(
                order_repository=order_repository,
                refund_policy_service=refund_policy_service,
            ),
        ]
    )
