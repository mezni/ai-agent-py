from typing import Protocol

from ai_agent_py.application.approval.dto import ApprovalView


class ApprovalRepository(Protocol):
    def save(self, approval: ApprovalView) -> None:
        ...

    def get_by_id(self, approval_id: str) -> ApprovalView | None:
        ...

    def update(self, approval: ApprovalView) -> None:
        ...

    def list_pending(self) -> list[ApprovalView]:
        ...
