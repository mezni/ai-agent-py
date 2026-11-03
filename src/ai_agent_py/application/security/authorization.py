from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)
from ai_agent_py.application.security.errors import (
    AuthorizationError,
    CustomerScopeError,
)
from ai_agent_py.application.security.permissions import Permission

ROLE_PERMISSIONS = {
    ActorRole.SUPPORT_AGENT: {
        Permission.READ_CUSTOMER,
        Permission.READ_ORDER,
        Permission.READ_POLICY,
        Permission.PROCESS_TICKET,
        Permission.ASSESS_REFUND,
    },
    ActorRole.SUPERVISOR: {
        Permission.READ_CUSTOMER,
        Permission.READ_ORDER,
        Permission.READ_POLICY,
        Permission.PROCESS_TICKET,
        Permission.ASSESS_REFUND,
        Permission.APPROVE_SENSITIVE_ACTION,
    },
    ActorRole.ADMIN: {
        Permission.ADMINISTER_SYSTEM,
        Permission.READ_POLICY,
    },
}


class AuthorizationService:
    def require_permission(
        self,
        actor: AuthenticatedActor,
        permission: Permission,
    ) -> None:
        permissions = ROLE_PERMISSIONS.get(actor.role, set())

        if permission not in permissions:
            raise AuthorizationError(
                f"Role '{actor.role.value}' lacks permission '{permission.value}'."
            )

    def require_customer_scope(
        self,
        actor: AuthenticatedActor,
        customer_id: str,
    ) -> None:
        if actor.customer_scope is None:
            # No implicit unrestricted access.
            raise CustomerScopeError("Actor has no explicit customer scope.")

        if customer_id not in actor.customer_scope:
            raise CustomerScopeError("Customer is outside the actor's authorized scope.")
