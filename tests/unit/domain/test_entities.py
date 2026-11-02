from datetime import date
from decimal import Decimal

import pytest

from ai_agent_py.domain.entities import Approval, Order, Ticket
from ai_agent_py.domain.enums import ApprovalStatus, OrderStatus, TicketStatus
from ai_agent_py.domain.value_objects import Money


@pytest.mark.unit
def test_order_contains_customer_and_amount() -> None:
    order = Order(
        order_id="ORD-001",
        customer_id="CUST-001",
        order_date=date(2026, 10, 1),
        status=OrderStatus.DELIVERED,
        total_amount=Money(Decimal("89.99")),
    )

    assert order.order_id == "ORD-001"
    assert order.customer_id == "CUST-001"
    assert order.total_amount.amount == Decimal("89.99")


@pytest.mark.unit
def test_ticket_has_initial_status() -> None:
    ticket = Ticket(
        ticket_id="TKT-001",
        customer_id="CUST-001",
        subject="Refund request",
        description="I would like a refund.",
        status=TicketStatus.OPEN,
    )

    assert ticket.status == TicketStatus.OPEN


@pytest.mark.unit
def test_pending_approval_does_not_require_reviewer() -> None:
    approval = Approval(
        approval_id="APR-001",
        assessment_id="ASSESS-001",
        status=ApprovalStatus.PENDING,
    )

    assert approval.status == ApprovalStatus.PENDING


@pytest.mark.unit
def test_approved_decision_requires_reviewer() -> None:
    with pytest.raises(ValueError):
        Approval(
            approval_id="APR-002",
            assessment_id="ASSESS-001",
            status=ApprovalStatus.APPROVED,
        )


@pytest.mark.unit
def test_approved_decision_records_reviewer() -> None:
    approval = Approval(
        approval_id="APR-003",
        assessment_id="ASSESS-001",
        status=ApprovalStatus.APPROVED,
        reviewer_id="SUP-001",
    )

    assert approval.reviewer_id == "SUP-001"
