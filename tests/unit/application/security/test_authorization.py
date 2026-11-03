import pytest

from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.authorization import (
    AuthorizationService,
)
from ai_agent_py.application.security.errors import (
    AuthorizationError,
    CustomerScopeError,
)
from ai_agent_py.application.security.permissions import Permission


def test_support_agent_can_process_ticket():
    service = AuthorizationService()
    actor = AuthenticatedActor(
        actor_id="agent-1",
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=frozenset({"customer-1"}),
    )

    service.require_permission(actor, Permission.PROCESS_TICKET)


def test_support_agent_cannot_approve_sensitive_action():
    service = AuthorizationService()
    actor = AuthenticatedActor(
        actor_id="agent-1",
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=frozenset({"customer-1"}),
    )

    with pytest.raises(AuthorizationError):
        service.require_permission(
            actor,
            Permission.APPROVE_SENSITIVE_ACTION,
        )


def test_customer_scope_denies_other_customer():
    service = AuthorizationService()
    actor = AuthenticatedActor(
        actor_id="agent-1",
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=frozenset({"customer-1"}),
    )

    with pytest.raises(CustomerScopeError):
        service.require_customer_scope(actor, "customer-2")


def test_missing_customer_scope_is_denied():
    service = AuthorizationService()
    actor = AuthenticatedActor(
        actor_id="agent-1",
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=None,
    )

    with pytest.raises(CustomerScopeError):
        service.require_customer_scope(actor, "customer-1")


def test_admin_does_not_automatically_get_approval_permission():
    service = AuthorizationService()
    actor = AuthenticatedActor(
        actor_id="admin-1",
        role=ActorRole.ADMIN,
        customer_scope=frozenset(),
    )

    with pytest.raises(AuthorizationError):
        service.require_permission(
            actor,
            Permission.APPROVE_SENSITIVE_ACTION,
        )
