from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ApprovalDecision(StrEnum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"


@dataclass(frozen=True)
class CreateApprovalRequest:
    requester_id: str
    ticket_id: str
    customer_id: str
    action_type: str
    resource_id: str
    reason: str
    requested_amount: str | None = None


@dataclass(frozen=True)
class ReviewApprovalRequest:
    approval_id: str
    reviewer_id: str
    decision: ApprovalDecision
    comment: str


@dataclass(frozen=True)
class ApprovalView:
    approval_id: str
    requester_id: str
    reviewer_id: str | None
    ticket_id: str
    customer_id: str
    action_type: str
    resource_id: str
    reason: str
    requested_amount: str | None
    status: str
    decision_comment: str | None
    created_at: datetime
    decided_at: datetime | None
    expires_at: datetime
