from ai_agent_py.application.approval.dto import ApprovalView


def is_action_authorized(
    approval: ApprovalView | None,
    *,
    expected_action_type: str,
    expected_resource_id: str,
) -> bool:
    """
    Return True only when a matching approval is approved.

    This checks authorization status only. It does not execute an action.
    """
    if approval is None:
        return False

    if approval.status != "APPROVED":
        return False

    if approval.action_type != expected_action_type:
        return False

    if approval.resource_id != expected_resource_id:
        return False

    if approval.decided_at is None or approval.reviewer_id is None:
        return False

    if approval.reviewer_id == approval.requester_id:
        return False

    return True
