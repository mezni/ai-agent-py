from datetime import UTC, datetime, timedelta

import pytest

from ai_agent_py.application.approval.dto import (
    ApprovalDecision,
    CreateApprovalRequest,
    ReviewApprovalRequest,
)
from ai_agent_py.application.approval.service import ApprovalService
from ai_agent_py.application.errors import (
    ApprovalAlreadyDecidedError,
    ApprovalExpiredError,
)
from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.approval_authorization import (
    ApprovalAuthorizationService,
)
from ai_agent_py.application.security.authorization import (
    AuthorizationService,
)
from ai_agent_py.infrastructure.persistence.in_memory_approval_repository import (
    InMemoryApprovalRepository,
)


@pytest.fixture
def repository():
    return InMemoryApprovalRepository()


@pytest.fixture
def service(repository):
    return ApprovalService(
        repository=repository,
        authorization_service=ApprovalAuthorizationService(
            AuthorizationService()
        ),
        ttl_minutes=60,
    )


@pytest.fixture
def requester():
    return AuthenticatedActor(
        actor_id="agent-1",
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=frozenset({"customer-1"}),
    )


@pytest.fixture
def supervisor():
    return AuthenticatedActor(
        actor_id="supervisor-1",
        role=ActorRole.SUPERVISOR,
        customer_scope=frozenset({"customer-1"}),
    )


def create_request():
    return CreateApprovalRequest(
        requester_id="agent-1",
        ticket_id="ticket-1",
        customer_id="customer-1",
        action_type="REFUND",
        resource_id="order-1",
        reason="Refund recommendation requires review.",
        requested_amount="75.00",
    )


def test_create_approval_starts_pending(service, requester):
    approval = service.create(create_request(), requester)

    assert approval.status == "PENDING"
    assert approval.reviewer_id is None
    assert approval.decided_at is None


def test_supervisor_can_approve(service, requester, supervisor):
    approval = service.create(create_request(), requester)

    result = service.review(
        request=ReviewApprovalRequest(
            approval_id=approval.approval_id,
            reviewer_id="ignored-client-value",
            decision=ApprovalDecision.APPROVE,
            comment="Reviewed and approved.",
        ),
        actor=supervisor,
    )

    assert result.status == "APPROVED"
    assert result.reviewer_id == "supervisor-1"
    assert result.decided_at is not None


def test_supervisor_can_reject(service, requester, supervisor):
    approval = service.create(create_request(), requester)

    result = service.review(
        request=ReviewApprovalRequest(
            approval_id=approval.approval_id,
            reviewer_id="ignored-client-value",
            decision=ApprovalDecision.REJECT,
            comment="Insufficient evidence.",
        ),
        actor=supervisor,
    )

    assert result.status == "REJECTED"


def test_approval_cannot_be_decided_twice(service, requester, supervisor):
    approval = service.create(create_request(), requester)

    service.review(
        request=ReviewApprovalRequest(
            approval_id=approval.approval_id,
            reviewer_id="ignored",
            decision=ApprovalDecision.APPROVE,
            comment="Approved.",
        ),
        actor=supervisor,
    )

    with pytest.raises(ApprovalAlreadyDecidedError):
        service.review(
            request=ReviewApprovalRequest(
                approval_id=approval.approval_id,
                reviewer_id="ignored",
                decision=ApprovalDecision.REJECT,
                comment="Changed my mind.",
            ),
            actor=supervisor,
        )


def test_expired_approval_cannot_be_approved(
    repository,
    requester,
    supervisor,
):
    service = ApprovalService(
        repository=repository,
        authorization_service=ApprovalAuthorizationService(
            AuthorizationService()
        ),
        ttl_minutes=1,
    )
    approval = service.create(create_request(), requester)

    expired = approval.__class__(
        **{
            **approval.__dict__,
            "expires_at": datetime.now(UTC) - timedelta(seconds=1),
        }
    )
    repository.update(expired)

    with pytest.raises(ApprovalExpiredError):
        service.review(
            request=ReviewApprovalRequest(
                approval_id=approval.approval_id,
                reviewer_id="ignored",
                decision=ApprovalDecision.APPROVE,
                comment="Approved.",
            ),
            actor=supervisor,
        )

    assert repository.get_by_id(approval.approval_id).status == "EXPIRED"
