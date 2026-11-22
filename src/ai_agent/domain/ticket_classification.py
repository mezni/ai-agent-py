from typing import Literal

from pydantic import BaseModel, ConfigDict

TicketCategory = Literal[
    "order_status",
    "refund",
    "technical_support",
    "account",
    "general",
]


class TicketClassification(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    category: TicketCategory
    order_id: str | None
    needs_order_lookup: bool
