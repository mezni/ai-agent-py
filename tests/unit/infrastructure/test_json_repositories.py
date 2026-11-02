import json
from datetime import date
from decimal import Decimal

import pytest

from ai_agent_py.domain.enums import OrderStatus, TicketStatus
from ai_agent_py.domain.value_objects import Money
from ai_agent_py.infrastructure.persistence.json_repositories import (
    FixtureDataError,
    JsonCustomerRepository,
    JsonOrderRepository,
    JsonTicketRepository,
)


@pytest.mark.unit
def test_customer_repository_returns_customer(tmp_path) -> None:
    fixture = tmp_path / "customers.json"
    fixture.write_text(
        json.dumps(
            [
                {
                    "customer_id": "CUST-001",
                    "email": "customer@example.test",
                }
            ]
        ),
        encoding="utf-8",
    )

    repository = JsonCustomerRepository(fixture)
    customer = repository.get_by_id("CUST-001")

    assert customer is not None
    assert customer.customer_id == "CUST-001"
    assert customer.email == "customer@example.test"


@pytest.mark.unit
def test_customer_repository_returns_none_when_missing(tmp_path) -> None:
    fixture = tmp_path / "customers.json"
    fixture.write_text("[]", encoding="utf-8")

    repository = JsonCustomerRepository(fixture)

    assert repository.get_by_id("CUST-404") is None


@pytest.mark.unit
def test_order_repository_maps_json_to_domain_entity(tmp_path) -> None:
    fixture = tmp_path / "orders.json"
    fixture.write_text(
        json.dumps(
            [
                {
                    "order_id": "ORD-001",
                    "customer_id": "CUST-001",
                    "order_date": "2026-10-01",
                    "status": "DELIVERED",
                    "total_amount": "89.99",
                    "currency": "CAD",
                }
            ]
        ),
        encoding="utf-8",
    )

    repository = JsonOrderRepository(fixture)
    order = repository.get_by_id("ORD-001")

    assert order is not None
    assert order.order_date == date(2026, 10, 1)
    assert order.status == OrderStatus.DELIVERED
    assert order.total_amount == Money(Decimal("89.99"))


@pytest.mark.unit
def test_order_repository_filters_by_customer(tmp_path) -> None:
    fixture = tmp_path / "orders.json"
    fixture.write_text(
        json.dumps(
            [
                {
                    "order_id": "ORD-001",
                    "customer_id": "CUST-001",
                    "order_date": "2026-10-01",
                    "status": "DELIVERED",
                    "total_amount": "89.99",
                    "currency": "CAD",
                },
                {
                    "order_id": "ORD-002",
                    "customer_id": "CUST-002",
                    "order_date": "2026-10-02",
                    "status": "PROCESSING",
                    "total_amount": "25.00",
                    "currency": "CAD",
                },
            ]
        ),
        encoding="utf-8",
    )

    repository = JsonOrderRepository(fixture)
    orders = repository.get_by_customer_id("CUST-001")

    assert len(orders) == 1
    assert orders[0].order_id == "ORD-001"


@pytest.mark.unit
def test_ticket_repository_maps_json_to_domain_entity(tmp_path) -> None:
    fixture = tmp_path / "tickets.json"
    fixture.write_text(
        json.dumps(
            [
                {
                    "ticket_id": "TKT-001",
                    "customer_id": "CUST-001",
                    "subject": "Refund request",
                    "description": "Please review my refund request.",
                    "status": "OPEN",
                }
            ]
        ),
        encoding="utf-8",
    )

    repository = JsonTicketRepository(fixture)
    ticket = repository.get_by_id("TKT-001")

    assert ticket is not None
    assert ticket.status == TicketStatus.OPEN
    assert ticket.subject == "Refund request"


@pytest.mark.unit
def test_repository_rejects_invalid_json(tmp_path) -> None:
    fixture = tmp_path / "customers.json"
    fixture.write_text("{invalid json", encoding="utf-8")

    repository = JsonCustomerRepository(fixture)

    with pytest.raises(FixtureDataError):
        repository.get_by_id("CUST-001")


@pytest.mark.unit
def test_repository_rejects_non_array_json(tmp_path) -> None:
    fixture = tmp_path / "customers.json"
    fixture.write_text('{"customer_id": "CUST-001"}', encoding="utf-8")

    repository = JsonCustomerRepository(fixture)

    with pytest.raises(FixtureDataError):
        repository.get_by_id("CUST-001")


@pytest.mark.unit
def test_repository_rejects_missing_fixture(tmp_path) -> None:
    fixture = tmp_path / "missing.json"
    repository = JsonCustomerRepository(fixture)

    with pytest.raises(FixtureDataError):
        repository.get_by_id("CUST-001")
