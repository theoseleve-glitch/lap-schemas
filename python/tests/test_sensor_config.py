import pytest
from pydantic import ValidationError

from lap_schemas.v1.sensor_config import SensorConfig, SensorConfigSnapshot


def test_sensor_config_snapshot_accepts_empty() -> None:
    snap = SensorConfigSnapshot()
    assert snap.sensors == ()
    assert snap.hardware_id is None
    assert snap.firmware_version is None


def test_sensor_config_snapshot_with_sensors_and_hardware() -> None:
    snap = SensorConfigSnapshot(
        sensors=(
            SensorConfig(name="gps", sample_rate_hz=10.0),
            SensorConfig(name="imu", sample_rate_hz=100.0),
        ),
        hardware_id="RB-12345",
        firmware_version="1.2.3",
    )
    assert len(snap.sensors) == 2
    assert snap.sensors[0].name == "gps"
    assert snap.sensors[1].sample_rate_hz == 100.0
    assert snap.hardware_id == "RB-12345"


def test_sensor_config_snapshot_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        SensorConfigSnapshot(**{"unknown_field": 1})
