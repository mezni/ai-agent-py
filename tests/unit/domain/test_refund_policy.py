from datetime import date
from decimal import Decimal

import pytest

from ai_agent_py.domain.enums import (
    ImageVerificationStatus,
    RefundEligibility,
)
from ai_agent_py.domain.services.refund_policy import RefundPolicyService
from ai_agent_py.domain.value_objects import Money


@pytest.fixture
def policy() -> RefundPolicyService:
    return RefundPolicyService()


@pytest.fixture
def base_request() -> dict:
    return {
        "assessment_id": "ASSESS-001",
        "order_id": "ORD-001",
        "order_date": date(2026, 10, 1),
        "requested_date": date(2026, 10, 15),
        "requested_amount": Money(Decimal("89.99")),
    }


@pytest.mark.unit
def test_refund_is_eligible_within_return_window(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.ELIGIBLE


@pytest.mark.unit
def test_refund_is_eligible_on_day_30(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["requested_date"] = date(2026, 10, 31)

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.ELIGIBLE


@pytest.mark.unit
def test_refund_is_ineligible_after_day_30(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["requested_date"] = date(2026, 11, 1)

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.INELIGIBLE


@pytest.mark.unit
def test_refund_is_ineligible_above_cap(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["requested_amount"] = Money(Decimal("100.01"))

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.INELIGIBLE


@pytest.mark.unit
def test_refund_is_ineligible_for_negative_amount(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["requested_amount"] = Money(Decimal("-10.00"))

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.INELIGIBLE


@pytest.mark.unit
def test_damaged_goods_require_image_verification(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["damaged"] = True

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.REQUIRES_VERIFICATION


@pytest.mark.unit
def test_verified_damaged_goods_can_be_eligible(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["damaged"] = True
    base_request["image_verification"] = ImageVerificationStatus.VERIFIED

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.ELIGIBLE


@pytest.mark.unit
def test_rejected_image_verification_requires_valid_verification(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    base_request["damaged"] = True
    base_request["image_verification"] = ImageVerificationStatus.REJECTED

    result = policy.assess(**base_request)

    assert result.eligibility == RefundEligibility.REQUIRES_VERIFICATION


@pytest.mark.unit
def test_refund_assessment_records_policy_version(
    policy: RefundPolicyService,
    base_request: dict,
) -> None:
    result = policy.assess(**base_request)

    assert result.policy_version == "1.0.0"
