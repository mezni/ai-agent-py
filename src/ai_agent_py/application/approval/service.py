from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from ai_agent_py.application.approval.dto import (
    ApprovalDecision,
    ApprovalView,
    CreateApprovalRequest,
    ReviewApprovalRequest,
)
from ai_agent_py.application.errors import (
    ApprovalAlreadyDecidedError,
    ApprovalExpiredError,
    ApprovalNotFoundError,
    InvalidApprovalRequestError,
)
from ai_agent_py.application.interfaces.approval_repository import (
    ApprovalRepository,
)
from ai_agent_py.application.security.actor import AuthenticatedActor
from ai_agent_py.application.security.approval_authorization import (
    ApprovalAuthorizationService,
)


class ApprovalService:
    def __init__(
        self,
        *,
        repository: ApprovalRepository,
        authorization_service: ApprovalAuthorizationService,
        ttl_minutes: int = 60,
    ) -> None:
        if ttl_minutes <= 0:
            raise ValueError("ttl_minutes must be positive.")

        self._repository = repository
        self._authorization_service = authorization_service
        self._ttl = timedelta(minutes=ttl_minutes)

    def create(
        self,
        request: CreateApprovalRequest,
        actor: AuthenticatedActor,
    ) -> ApprovalView:
        self._authorization_service.require_request_authority(
            actor=actor,
            customer_id=request.customer_id,
        )

        if request.requester_id != actor.actor_id:
            raise InvalidApprovalRequestError(
                "Requester identity must match the authenticated actor."
            )

        self._validate_create_request(request)

        now = datetime.now(UTC)

        approval = ApprovalView(
            approval_id=str(uuid4()),
            requester_id=request.requester_id,
            reviewer_id=None,
            ticket_id=request.ticket_id,
            customer_id=request.customer_id,
            action_type=request.action_type,
            resource_id=request.resource_id,
            reason=request.reason.strip(),
            requested_amount=request.requested_amount,
            status="PENDING",
            decision_comment=None,
            created_at=now,
            decided_at=None,
            expires_at=now + self._ttl,
        )

        self._repository.save(approval)
        return approval

    def review(
        self,
        *,
        request: ReviewApprovalRequest,
        actor: AuthenticatedActor,
    ) -> ApprovalView:
        self._validate_review_request(request)

        approval = self._repository.get_by_id(request.approval_id)
        if approval is None:
            raise ApprovalNotFoundError(
                f"Approval '{request.approval_id}' was not found."
            )

        self._authorization_service.require_approval_authority(
            actor=actor,
            requester_id=approval.requester_id,
        )

        self._authorization_service.require_customer_scope(
            actor=actor,
            customer_id=approval.customer_id,
        )

        if approval.status != "PENDING":
            raise ApprovalAlreadyDecidedError(
                "Only pending approvals can be reviewed."
            )

        now = datetime.now(UTC)

        if now >= approval.expires_at:
            expired = replace(
                approval,
                status="EXPIRED",
            )
            self._repository.update(expired)
            raise ApprovalExpiredError(
                "Approval request has expired."
            )

        new_status = (
            "APPROVED"
            if request.decision == ApprovalDecision.APPROVE
            else "REJECTED"
        )

        updated = replace(
            approval,
            reviewer_id=actor.actor_id,
            status=new_status,
            decision_comment=request.comment.strip(),
            decided_at=now,
        )

        self._repository.update(updated)
        return updated

    def get(self, approval_id: str) -> ApprovalView:
        approval = self._repository.get_by_id(approval_id)

        if approval is None:
            raise ApprovalNotFoundError(
                f"Approval '{approval_id}' was not found."
            )

        return approval

    @staticmethod
    def _validate_create_request(
        request: CreateApprovalRequest,
    ) -> None:
        values = {
            "requester_id": request.requester_id,
            "ticket_id": request.ticket_id,
            "customer_id": request.customer_id,
            "action_type": request.action_type,
            "resource_id": request.resource_id,
            "reason": request.reason,
        }

        for name, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidApprovalRequestError(
                    f"{name} must be a non-empty string."
                )

        if (
            request.requested_amount is not None
            and not request.requested_amount.strip()
        ):
            raise InvalidApprovalRequestError(
                "requested_amount must not be empty."
            )

    @staticmethod
    def _validate_review_request(
        request: ReviewApprovalRequest,
    ) -> None:
        if not request.approval_id.strip():
            raise InvalidApprovalRequestError(
                "approval_id must not be empty."
            )

        if not request.comment.strip():
            raise InvalidApprovalRequestError(
                "A review comment is required."
            )

        if not isinstance(request.decision, ApprovalDecision):
            raise InvalidApprovalRequestError(
                "Unsupported approval decision."
            )
