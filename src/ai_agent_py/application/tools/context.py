from dataclasses import dataclass


@dataclass(frozen=True)
class ToolExecutionContext:
    actor_id: str
    actor_role: str
    customer_id: str
    ticket_id: str
