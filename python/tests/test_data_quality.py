import pytest
from pydantic import ValidationError

from lap_schemas.v1.data_quality import DataQuality


def test_data_quality_full_real_session() -> None:
    dq = DataQuality(
        score=85.0,
        gps_fix_quality=0.95,
        gps_satellite_count_avg=12,
        channel_completeness=98.0,
        sample_gaps_count=2,
        sample_rate_stability=0.03,
        warnings=("gap at T3",),
        recommendations=("enable CAN filter",),
        usable_for_overlays=True,
        usable_for_long_term_coaching=True,
    )
    assert dq.score == 85.0
    assert dq.gps_fix_quality == 0.95
    assert dq.gps_satellite_count_avg == 12
    assert dq.warnings == ("gap at T3",)
    assert dq.usable_for_long_term_coaching is True


def test_data_quality_minimal_sim_session() -> None:
    dq = DataQuality(
        score=92.0,
        channel_completeness=100.0,
        sample_gaps_count=0,
        sample_rate_stability=0.01,
        usable_for_overlays=True,
        usable_for_long_term_coaching=True,
    )
    assert dq.gps_fix_quality is None
    assert dq.gps_satellite_count_avg is None
    assert dq.warnings == ()
    assert dq.recommendations == ()


def test_data_quality_rejects_score_above_100() -> None:
    with pytest.raises(ValidationError):
        DataQuality(
            score=150.0,
            channel_completeness=50.0,
            sample_gaps_count=0,
            sample_rate_stability=0.0,
            usable_for_overlays=False,
            usable_for_long_term_coaching=False,
        )
