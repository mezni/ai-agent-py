from dataclasses import dataclass
from datetime import date, datetime

from ai_agent_py.domain.enums import (
    AgentIntent,
    ApprovalStatus,
    ExecutionStatus,
    OrderStatus,
    TicketStatus,
    ToolExecutionStatus,
)
from ai_agent_py.domain.value_objects import Money


@dataclass(frozen=True)
class Customer:
    customer_id: str
    email: str


@dataclass(frozen=True)
class Order:
    order_id: str
    customer_id: str
    order_date: date
    status: OrderStatus
    total_amount: Money


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    customer_id: str
    subject: str
    description: str
    status: TicketStatus


@dataclass(frozen=True)
class AgentDecision:
    decision_id: str
    ticket_id: str
    intent: AgentIntent
    rationale: str


@dataclass(frozen=True)
class RefundAssessment:
    assessment_id: str
    order_id: str
    eligibility: str
    requested_amount: Money
    reason: str
    policy_version: str


@dataclass(frozen=True)
class Approval:
    approval_id: str
    assessment_id: str
    status: ApprovalStatus
    reviewer_id: str | None = None

    def __post_init__(self) -> None:
        if (
            self.status
            in {
                ApprovalStatus.APPROVED,
                ApprovalStatus.REJECTED,
            }
            and not self.reviewer_id
        ):
            raise ValueError("A reviewer ID is required for a final approval decision.")


@dataclass(frozen=True)
class AgentExecution:
    execution_id: str
    ticket_id: str
    status: ExecutionStatus
    started_at: datetime


@dataclass(frozen=True)
class ToolExecution:
    tool_execution_id: str
    tool_name: str
    status: ToolExecutionStatus
    customer_id: str
