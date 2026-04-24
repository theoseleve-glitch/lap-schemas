import pytest
from pydantic import ValidationError

from lap_schemas.v1.telemetry_sample import TelemetrySample


def test_telemetry_sample_sim_with_irsdk_clock() -> None:
    sample = TelemetrySample(
        t_source_ns=123_456_789,
        t_canonical_ns=123_456_789,
        t_source_clock="irsdk_tick",
        channels={"speed_mps": 68.4, "throttle_pct": 0.92, "brake_pct": 0.0},
    )
    assert sample.t_source_ns == 123_456_789
    assert sample.t_source_clock == "irsdk_tick"
    assert sample.channels["speed_mps"] == 68.4


def test_telemetry_sample_real_with_racebox_clock() -> None:
    sample = TelemetrySample(
        t_source_ns=1_000_000,
        t_canonical_ns=1_050_000,
        t_source_clock="racebox_gnss",
        channels={"lat": 43.2331, "lon": 5.4413, "speed_mps": 72.1},
    )
    assert sample.t_source_ns == 1_000_000
    assert sample.t_canonical_ns == 1_050_000
    assert sample.t_source_clock == "racebox_gnss"


def test_telemetry_sample_rejects_unknown_clock() -> None:
    with pytest.raises(ValidationError):
        TelemetrySample(
            t_source_ns=0,
            t_canonical_ns=0,
            t_source_clock="wall_clock",  # not in the allowed literal set
            channels={},
        )
