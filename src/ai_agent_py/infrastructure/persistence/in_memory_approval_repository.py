from threading import RLock

from ai_agent_py.application.approval.dto import ApprovalView


class InMemoryApprovalRepository:
    """Thread-safe, process-local approval storage."""

    def __init__(self) -> None:
        self._approvals: dict[str, ApprovalView] = {}
        self._lock = RLock()

    def save(self, approval: ApprovalView) -> None:
        with self._lock:
            if approval.approval_id in self._approvals:
                raise ValueError("Approval ID already exists.")

            self._approvals[approval.approval_id] = approval

    def get_by_id(self, approval_id: str) -> ApprovalView | None:
        with self._lock:
            return self._approvals.get(approval_id)

    def update(self, approval: ApprovalView) -> None:
        with self._lock:
            if approval.approval_id not in self._approvals:
                raise KeyError("Approval does not exist.")

            self._approvals[approval.approval_id] = approval

    def list_pending(self) -> list[ApprovalView]:
        with self._lock:
            return [
                approval
                for approval in self._approvals.values()
                if approval.status == "PENDING"
            ]
