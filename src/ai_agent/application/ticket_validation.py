from ai_agent.application.errors import (
    LLMValidationError,
)
from ai_agent.domain.ticket_classification import (
    TicketClassification,
)


def validate_ticket_classification(
    result: TicketClassification,
) -> TicketClassification:
    if result.needs_order_lookup and result.order_id is None:
        raise LLMValidationError("Order lookup requires an order ID.")

    if result.needs_order_lookup and result.category != "order_status":
        raise LLMValidationError(
            "Order lookup is only allowed for order_status in this application."
        )

    return result
