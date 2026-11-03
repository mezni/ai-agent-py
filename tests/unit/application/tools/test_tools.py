from types import SimpleNamespace

import pytest

from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.authorization import AuthorizationService
from ai_agent_py.application.security.errors import AuthorizationError
from ai_agent_py.application.tools import build_tool_registry
from ai_agent_py.application.tools.business_policy_lookup import (
    BusinessPolicyLookupTool,
)
from ai_agent_py.application.tools.context import ToolExecutionContext
from ai_agent_py.application.tools.contracts import ToolCall, ToolStatus
from ai_agent_py.application.tools.customer_lookup import CustomerLookupTool
from ai_agent_py.application.tools.order_lookup import OrderLookupTool
from ai_agent_py.application.tools.refund_eligibility import (
    RefundEligibilityAssessmentTool,
)


class FakeCustomerRepository:
    def __init__(self, customers) -> None:
        self._customers = {customer.id: customer for customer in customers}

    def get_by_id(self, customer_id):
        return self._customers.get(customer_id)


class FakeOrderRepository:
    def __init__(self, orders) -> None:
        self._orders = {order.id: order for order in orders}

    def get_by_id(self, order_id):
        return self._orders.get(order_id)


class FakePolicyRepository:
    def __init__(self, policies) -> None:
        self._policies = policies

    def get_by_type(self, policy_type):
        return self._policies.get(policy_type)


class FakeRefundPolicyService:
    def assess(self, *, order, requested_amount, reason, image_verification_status):
        return SimpleNamespace(
            eligibility="ELIGIBLE",
            approved_amount=requested_amount,
            policy_version="1.0.0",
            reasons=("Within the refund window.",),
        )


class DenyingAuthorizationService:
    def require_permission(self, actor, permission):
        raise AuthorizationError("Denied for test.")

    def require_customer_scope(self, actor, customer_id):
        raise AuthorizationError("Denied for test.")


def build_actor(
    *,
    role: ActorRole = ActorRole.SUPPORT_AGENT,
    scope: tuple[str, ...] | None = ("CUST-1",),
) -> AuthenticatedActor:
    return AuthenticatedActor(
        actor_id="agent-1",
        role=role,
        customer_scope=None if scope is None else frozenset(scope),
    )


def build_context(actor: AuthenticatedActor | None = None) -> ToolExecutionContext:
    return ToolExecutionContext(
        actor=actor or build_actor(),
        customer_id="CUST-1",
        ticket_id="ticket-1",
    )


def build_customer_tool() -> CustomerLookupTool:
    return CustomerLookupTool(
        FakeCustomerRepository([SimpleNamespace(id="CUST-1", name="Ada", tier="GOLD")]),
        AuthorizationService(),
    )


def build_order_tool() -> OrderLookupTool:
    return OrderLookupTool(
        FakeOrderRepository(
            [
                SimpleNamespace(
                    id="ORDER-1",
                    customer_id="CUST-1",
                    status="DELIVERED",
                    total="10.00",
                ),
                SimpleNamespace(
                    id="ORDER-2",
                    customer_id="CUST-2",
                    status="DELIVERED",
                    total="20.00",
                ),
            ]
        ),
        AuthorizationService(),
    )


def build_refund_tool() -> RefundEligibilityAssessmentTool:
    return RefundEligibilityAssessmentTool(
        order_repository=FakeOrderRepository(
            [
                SimpleNamespace(
                    id="ORDER-1",
                    customer_id="CUST-1",
                    status="DELIVERED",
                    total="10.00",
                ),
                SimpleNamespace(
                    id="ORDER-2",
                    customer_id="CUST-2",
                    status="DELIVERED",
                    total="20.00",
                ),
            ]
        ),
        refund_policy_service=FakeRefundPolicyService(),
        authorization_service=AuthorizationService(),
    )


@pytest.mark.unit
def test_customer_lookup_returns_authorized_customer():
    result = build_customer_tool().execute(
        ToolCall("customer_lookup", {"customer_id": "CUST-1"}),
        build_context(),
    )

    assert result.status == ToolStatus.SUCCESS
    assert result.data == {
        "customer_id": "CUST-1",
        "display_name": "Ada",
        "tier": "GOLD",
    }


@pytest.mark.unit
def test_customer_lookup_denies_missing_permission():
    result = build_customer_tool().execute(
        ToolCall("customer_lookup", {"customer_id": "CUST-1"}),
        build_context(build_actor(role=ActorRole.ADMIN)),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_customer_lookup_denies_out_of_scope_customer():
    result = build_customer_tool().execute(
        ToolCall("customer_lookup", {"customer_id": "CUST-2"}),
        build_context(),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_customer_lookup_rejects_invalid_arguments():
    result = build_customer_tool().execute(
        ToolCall("customer_lookup", {}),
        build_context(),
    )

    assert result.status == ToolStatus.INVALID_ARGUMENTS


@pytest.mark.unit
def test_customer_lookup_returns_not_found_within_scope():
    tool = CustomerLookupTool(
        FakeCustomerRepository([]),
        AuthorizationService(),
    )

    result = tool.execute(
        ToolCall("customer_lookup", {"customer_id": "CUST-1"}),
        build_context(),
    )

    assert result.status == ToolStatus.NOT_FOUND


@pytest.mark.unit
def test_order_lookup_returns_authorized_order():
    result = build_order_tool().execute(
        ToolCall("order_lookup", {"order_id": "ORDER-1"}),
        build_context(),
    )

    assert result.status == ToolStatus.SUCCESS
    assert result.data["order_id"] == "ORDER-1"


@pytest.mark.unit
def test_order_lookup_denies_missing_permission():
    result = build_order_tool().execute(
        ToolCall("order_lookup", {"order_id": "ORDER-1"}),
        build_context(build_actor(role=ActorRole.ADMIN)),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_order_lookup_denies_order_outside_actor_scope():
    result = build_order_tool().execute(
        ToolCall("order_lookup", {"order_id": "ORDER-2"}),
        build_context(),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_order_lookup_denies_order_outside_context():
    result = build_order_tool().execute(
        ToolCall("order_lookup", {"order_id": "ORDER-2"}),
        build_context(build_actor(scope=("CUST-1", "CUST-2"))),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_order_lookup_rejects_invalid_arguments_and_missing_order():
    tool = build_order_tool()

    invalid = tool.execute(ToolCall("order_lookup", {}), build_context())
    missing = tool.execute(
        ToolCall("order_lookup", {"order_id": "ORDER-404"}),
        build_context(),
    )

    assert invalid.status == ToolStatus.INVALID_ARGUMENTS
    assert missing.status == ToolStatus.NOT_FOUND


@pytest.mark.unit
def test_business_policy_lookup_returns_policy():
    tool = BusinessPolicyLookupTool(
        FakePolicyRepository({"refund": SimpleNamespace(version="1.0.0", content="Refund policy")}),
        AuthorizationService(),
    )

    result = tool.execute(
        ToolCall("business_policy_lookup", {"policy_type": "refund"}),
        build_context(),
    )

    assert result.status == ToolStatus.SUCCESS
    assert result.data == {
        "policy_type": "refund",
        "policy_version": "1.0.0",
        "content": "Refund policy",
    }


@pytest.mark.unit
def test_business_policy_lookup_denies_missing_permission():
    tool = BusinessPolicyLookupTool(
        FakePolicyRepository({}),
        DenyingAuthorizationService(),
    )

    result = tool.execute(
        ToolCall("business_policy_lookup", {"policy_type": "refund"}),
        build_context(),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_business_policy_lookup_rejects_invalid_arguments_and_missing_policy():
    tool = BusinessPolicyLookupTool(
        FakePolicyRepository({}),
        AuthorizationService(),
    )

    invalid = tool.execute(ToolCall("business_policy_lookup", {}), build_context())
    missing = tool.execute(
        ToolCall("business_policy_lookup", {"policy_type": "missing"}),
        build_context(),
    )

    assert invalid.status == ToolStatus.INVALID_ARGUMENTS
    assert missing.status == ToolStatus.NOT_FOUND


@pytest.mark.unit
def test_refund_assessment_returns_bounded_result():
    result = build_refund_tool().execute(
        ToolCall(
            "refund_eligibility_assessment",
            {"order_id": "ORDER-1", "reason": "Damaged item"},
        ),
        build_context(),
    )

    assert result.status == ToolStatus.SUCCESS
    assert result.data["order_id"] == "ORDER-1"
    assert result.data["eligibility"] == "ELIGIBLE"


@pytest.mark.unit
def test_refund_assessment_denies_missing_permission():
    result = build_refund_tool().execute(
        ToolCall(
            "refund_eligibility_assessment",
            {"order_id": "ORDER-1", "reason": "Damaged item"},
        ),
        build_context(build_actor(role=ActorRole.ADMIN)),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_refund_assessment_denies_order_outside_scope():
    result = build_refund_tool().execute(
        ToolCall(
            "refund_eligibility_assessment",
            {"order_id": "ORDER-2", "reason": "Damaged item"},
        ),
        build_context(),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_refund_assessment_denies_order_outside_context():
    result = build_refund_tool().execute(
        ToolCall(
            "refund_eligibility_assessment",
            {"order_id": "ORDER-2", "reason": "Damaged item"},
        ),
        build_context(build_actor(scope=("CUST-1", "CUST-2"))),
    )

    assert result.status == ToolStatus.DENIED


@pytest.mark.unit
def test_refund_assessment_rejects_invalid_arguments_and_missing_order():
    tool = build_refund_tool()

    invalid = tool.execute(
        ToolCall("refund_eligibility_assessment", {"order_id": "ORDER-1"}),
        build_context(),
    )
    missing = tool.execute(
        ToolCall(
            "refund_eligibility_assessment",
            {"order_id": "ORDER-404", "reason": "Damaged item"},
        ),
        build_context(),
    )

    assert invalid.status == ToolStatus.INVALID_ARGUMENTS
    assert missing.status == ToolStatus.NOT_FOUND


@pytest.mark.unit
def test_build_tool_registry_injects_shared_authorization_service():
    service = AuthorizationService()
    registry = build_tool_registry(
        customer_repository=FakeCustomerRepository([]),
        order_repository=FakeOrderRepository([]),
        policy_repository=FakePolicyRepository({}),
        refund_policy_service=FakeRefundPolicyService(),
        authorization_service=service,
    )

    assert registry.tool_names == (
        "business_policy_lookup",
        "customer_lookup",
        "order_lookup",
        "refund_eligibility_assessment",
    )
    assert all(tool._authorization_service is service for tool in registry._tools.values())


@pytest.mark.unit
def test_build_tool_registry_creates_authorization_service_by_default():
    registry = build_tool_registry(
        customer_repository=FakeCustomerRepository([]),
        order_repository=FakeOrderRepository([]),
        policy_repository=FakePolicyRepository({}),
        refund_policy_service=FakeRefundPolicyService(),
    )

    assert "customer_lookup" in registry.tool_names
