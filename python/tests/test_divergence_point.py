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


# -- T017 (sprint2-backend): edge-case validation pins ------------


def test_divergence_point_rejects_negative_track_distance() -> None:
    """Track distance is meters along the lap from start/finish —
    a negative value is nonsensical (you can't be "before" the
    line). Pins the ge=0 constraint."""
    with pytest.raises(ValidationError):
        DivergencePoint(
            track_distance_m=-1.0,
            metric="brake_pressure_peak",
            sim_value=0.5,
            real_value=0.5,
            divergence_type="shape",
        )


def test_divergence_point_rejects_empty_metric() -> None:
    """A divergence point without a named metric is meaningless —
    the consumer needs the metric label to render the chart axis
    or join back to a feature definition."""
    with pytest.raises(ValidationError):
        DivergencePoint(
            track_distance_m=100.0,
            metric="",
            sim_value=0.5,
            real_value=0.5,
            divergence_type="shape",
        )


def test_divergence_point_accepts_both_divergence_type() -> None:
    """`both` is in the Literal; covers the 'shape AND intensity
    diverged' case. Existing tests covered shape and intensity
    individually."""
    dp = DivergencePoint(
        track_distance_m=200.0,
        metric="apex_speed_mps",
        sim_value=42.0,
        real_value=38.0,
        divergence_type="both",
    )
    assert dp.divergence_type == "both"


def test_divergence_point_round_trip_json() -> None:
    original = DivergencePoint(
        track_distance_m=1500.5,
        metric="throttle_pct",
        sim_value=0.95,
        real_value=0.7,
        divergence_type="intensity",
    )
    revived = DivergencePoint.model_validate_json(original.model_dump_json())
    assert revived == original


def test_divergence_point_rejects_extra_fields() -> None:
    """`extra="forbid"` pins the wire shape — adding a field on the
    consumer side without bumping the schema version is a typo
    or a contract drift."""
    with pytest.raises(ValidationError):
        DivergencePoint(  # type: ignore[call-arg]
            track_distance_m=100.0,
            metric="brake_pressure_peak",
            sim_value=0.5,
            real_value=0.5,
            divergence_type="shape",
            unknown_field="oops",
        )
