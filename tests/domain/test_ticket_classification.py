import pytest
from pydantic import ValidationError

from ai_agent.domain.ticket_classification import (
    TicketClassification,
)


def test_valid_classification():
    result = TicketClassification(
        category="order_status",
        order_id="4821",
        needs_order_lookup=True,
    )

    assert result.category == "order_status"
    assert result.order_id == "4821"
    assert result.needs_order_lookup is True


def test_order_id_can_be_none():
    result = TicketClassification(
        category="general",
        order_id=None,
        needs_order_lookup=False,
    )

    assert result.order_id is None


def test_invalid_category():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="shipping_problem",
            order_id="4821",
            needs_order_lookup=True,
        )


def test_invalid_boolean():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="order_status",
            order_id="4821",
            needs_order_lookup="true",
        )


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="order_status",
            order_id="4821",
            needs_order_lookup=True,
            extra_field="unexpected",
        )


def test_missing_field_rejected():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="order_status",
            order_id="4821",
        )
