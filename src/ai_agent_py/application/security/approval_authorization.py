from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.errors import AuthorizationError
from ai_agent_py.application.security.permissions import Permission


class ApprovalAuthorizationService:
    def __init__(self, authorization_service) -> None:
        self._authorization_service = authorization_service

    def require_approval_authority(
        self,
        *,
        actor: AuthenticatedActor,
        requester_id: str,
    ) -> None:
        self._authorization_service.require_permission(
            actor,
            Permission.APPROVE_SENSITIVE_ACTION,
        )

        if actor.role != ActorRole.SUPERVISOR:
            raise AuthorizationError("Only an authorized supervisor may approve sensitive actions.")

        if actor.actor_id == requester_id:
            raise AuthorizationError("A requester cannot approve their own action.")

    def require_request_authority(
        self,
        *,
        actor: AuthenticatedActor,
        customer_id: str,
    ) -> None:
        self._authorization_service.require_permission(
            actor,
            Permission.PROCESS_TICKET,
        )
        self._authorization_service.require_customer_scope(
            actor,
            customer_id,
        )

    def require_customer_scope(
        self,
        *,
        actor: AuthenticatedActor,
        customer_id: str,
    ) -> None:
        self._authorization_service.require_customer_scope(
            actor,
            customer_id,
        )
