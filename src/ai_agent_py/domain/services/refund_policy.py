from datetime import date
from decimal import Decimal

from ai_agent_py.domain.entities import RefundAssessment
from ai_agent_py.domain.enums import (
    ImageVerificationStatus,
    RefundEligibility,
)
from ai_agent_py.domain.value_objects import Money


class RefundPolicyService:
    RETURN_WINDOW_DAYS = 30
    MAXIMUM_REFUND = Money(Decimal("100.00"))
    POLICY_VERSION = "1.0.0"

    def assess(
        self,
        *,
        assessment_id: str,
        order_id: str,
        order_date: date,
        requested_date: date,
        requested_amount: Money,
        damaged: bool = False,
        image_verification: ImageVerificationStatus = (ImageVerificationStatus.NOT_PROVIDED),
    ) -> RefundAssessment:
        if requested_amount.currency != "CAD":
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "Only CAD refunds are supported by this policy.",
            )

        if requested_amount.is_negative():
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "Refund amount cannot be negative.",
            )

        if requested_amount.amount == Decimal("0"):
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "Refund amount must be greater than zero.",
            )

        if requested_amount.is_greater_than(self.MAXIMUM_REFUND):
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "Requested amount exceeds the CAD 100 refund cap.",
            )

        days_since_order = (requested_date - order_date).days

        if days_since_order < 0:
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "Requested date cannot precede the order date.",
            )

        if days_since_order > self.RETURN_WINDOW_DAYS:
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.INELIGIBLE,
                requested_amount,
                "The 30-calendar-day return window has expired.",
            )

        if damaged and image_verification != ImageVerificationStatus.VERIFIED:
            return self._result(
                assessment_id,
                order_id,
                RefundEligibility.REQUIRES_VERIFICATION,
                requested_amount,
                "Damaged goods require valid image verification.",
            )

        return self._result(
            assessment_id,
            order_id,
            RefundEligibility.ELIGIBLE,
            requested_amount,
            "Refund satisfies the configured business policy.",
        )

    def _result(
        self,
        assessment_id: str,
        order_id: str,
        eligibility: RefundEligibility,
        requested_amount: Money,
        reason: str,
    ) -> RefundAssessment:
        return RefundAssessment(
            assessment_id=assessment_id,
            order_id=order_id,
            eligibility=eligibility,
            requested_amount=requested_amount,
            reason=reason,
            policy_version=self.POLICY_VERSION,
        )
