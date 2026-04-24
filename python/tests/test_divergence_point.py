import pytest
from pydantic import ValidationError

from lap_schemas.v1.divergence_point import DivergencePoint


def test_divergence_point_accepts_shape_divergence() -> None:
    dp = DivergencePoint(
        track_distance_m=1234.5,
        metric="brake_pressure_peak",
        sim_value=72.1,
        real_value=58.4,
        divergence_type="shape",
    )
    assert dp.divergence_type == "shape"
    assert dp.sim_value == 72.1
    assert dp.real_value == 58.4


def test_divergence_point_accepts_intensity_divergence() -> None:
    dp = DivergencePoint(
        track_distance_m=0.0,  # start/finish
        metric="apex_speed_mps",
        sim_value=40.2,
        real_value=40.3,
        divergence_type="intensity",
    )
    assert dp.divergence_type == "intensity"
    assert dp.track_distance_m == 0.0


def test_divergence_point_rejects_unknown_divergence_type() -> None:
    with pytest.raises(ValidationError):
        DivergencePoint(
            track_distance_m=500.0,
            metric="throttle_pct",
            sim_value=0.8,
            real_value=0.7,
            divergence_type="timing",  # not in allowed set
        )
