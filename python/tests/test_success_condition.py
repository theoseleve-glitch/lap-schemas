import pytest
from pydantic import ValidationError

from lap_schemas.v1.success_condition import SuccessCondition


def test_success_condition_accepts_gte_threshold() -> None:
    cond = SuccessCondition(
        metric="t1_trail_brake_release_pct",
        target_value=0.75,
        comparison="gte",
        target_pct=None,
        measurement_window="next_3_sessions",
    )
    assert cond.metric == "t1_trail_brake_release_pct"
    assert cond.comparison == "gte"
    assert cond.target_pct is None


def test_success_condition_accepts_within_pct_with_target() -> None:
    cond = SuccessCondition(
        metric="apex_speed_delta_mps",
        target_value=0.0,
        comparison="within_pct",
        target_pct=5.0,
        measurement_window="next_7_days",
    )
    assert cond.comparison == "within_pct"
    assert cond.target_pct == 5.0
    assert cond.measurement_window == "next_7_days"


def test_success_condition_rejects_unknown_comparison() -> None:
    with pytest.raises(ValidationError):
        SuccessCondition(
            metric="brake_peak_bar",
            target_value=70.0,
            comparison="approximately",  # not in allowed set
            target_pct=None,
            measurement_window="next_session",
        )
