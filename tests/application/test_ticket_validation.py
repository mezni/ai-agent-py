import pytest

from ai_agent.application.errors import (
    LLMValidationError,
)
from ai_agent.application.ticket_validation import (
    validate_ticket_classification,
)
from ai_agent.domain.ticket_classification import (
    TicketClassification,
)


def test_valid_order_status():
    result = TicketClassification(
        category="order_status",
        order_id="4821",
        needs_order_lookup=True,
    )

    validated = validate_ticket_classification(result)

    assert validated.order_id == "4821"


def test_lookup_without_order_id():
    result = TicketClassification(
        category="order_status",
        order_id=None,
        needs_order_lookup=True,
    )

    with pytest.raises(LLMValidationError):
        validate_ticket_classification(result)


def test_lookup_with_wrong_category():
    result = TicketClassification(
        category="refund",
        order_id="4821",
        needs_order_lookup=True,
    )

    with pytest.raises(LLMValidationError):
        validate_ticket_classification(result)


def test_no_lookup_allowed():
    result = TicketClassification(
        category="general",
        order_id=None,
        needs_order_lookup=False,
    )

    validated = validate_ticket_classification(result)

    assert validated.category == "general"
