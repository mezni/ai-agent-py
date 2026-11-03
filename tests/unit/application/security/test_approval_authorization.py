import pytest

from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.authorization import (
    AuthorizationService,
)
from ai_agent_py.application.security.approval_authorization import (
    ApprovalAuthorizationService,
)
from ai_agent_py.application.security.errors import AuthorizationError


def test_supervisor_can_approve_another_actors_request():
    service = ApprovalAuthorizationService(AuthorizationService())
    supervisor = AuthenticatedActor(
        actor_id="supervisor-1",
        role=ActorRole.SUPERVISOR,
        customer_scope=frozenset({"customer-1"}),
    )

    service.require_approval_authority(
        actor=supervisor,
        requester_id="agent-1",
    )


def test_supervisor_cannot_approve_own_request():
    service = ApprovalAuthorizationService(AuthorizationService())
    supervisor = AuthenticatedActor(
        actor_id="supervisor-1",
        role=ActorRole.SUPERVISOR,
        customer_scope=frozenset({"customer-1"}),
    )

    with pytest.raises(AuthorizationError):
        service.require_approval_authority(
            actor=supervisor,
            requester_id="supervisor-1",
        )
