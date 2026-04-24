from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.data_quality import DataQuality
from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.sensor_config import SensorConfigSnapshot
from lap_schemas.v1.session import SessionManifest
from lap_schemas.v1.session_record import SessionRecord


def _manifest() -> SessionManifest:
    return SessionManifest(
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        bundle_version="v2",
        capture_app="lap-coach-logger",
        capture_app_version="0.9.0",
        device_model="Desktop",
        device_os="Windows",
        device_os_version="11",
        source="iracing",
        sim_title="iracing",
        real_hardware=None,
        car_id=uuid6.uuid7(),
        track_id=uuid6.uuid7(),
        track_layout="gp",
        environment_tag=EnvironmentTag.SIM_PRACTICE,
        objective_tag=None,
        training_block_id=None,
        started_at=datetime(2026, 4, 24, 10, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 10, 30, tzinfo=timezone.utc),
        duration_seconds=1800.0,
        telemetry_checksums={"samples.bin": "sha256:abc"},
        total_samples=108000,
        sample_rate_hz=60.0,
        data_quality=DataQuality(
            score=95.0,
            channel_completeness=100.0,
            sample_gaps_count=0,
            sample_rate_stability=0.0,
            usable_for_overlays=True,
            usable_for_long_term_coaching=True,
        ),
        sensor_config=SensorConfigSnapshot(),
    )


def test_session_record_accepts_processed_payload() -> None:
    record = SessionRecord(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        manifest=_manifest(),
        processed_at=datetime(2026, 4, 24, 10, 35, tzinfo=timezone.utc),
        schema_version="v1",
        best_lap_ms=84_321,
        avg_lap_ms=85_900,
        peak_speed_mps=78.3,
        consistency_index=0.91,
        total_laps=12,
        valid_laps=11,
    )
    assert record.schema_version == "v1"
    assert record.best_lap_ms == 84_321
    assert record.valid_laps == 11


def test_session_record_allows_missing_metrics() -> None:
    # A session with no completed laps yet still produces a processed record.
    record = SessionRecord(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        manifest=_manifest(),
        processed_at=datetime(2026, 4, 24, 10, 35, tzinfo=timezone.utc),
        schema_version="v1",
    )
    assert record.best_lap_ms is None
    assert record.avg_lap_ms is None
    assert record.peak_speed_mps is None
    assert record.consistency_index is None
    assert record.total_laps == 0
    assert record.valid_laps == 0


def test_session_record_rejects_unknown_schema_version() -> None:
    with pytest.raises(ValidationError):
        SessionRecord(
            id=uuid6.uuid7(),
            session_id=uuid6.uuid7(),
            manifest=_manifest(),
            processed_at=datetime(2026, 4, 24, 10, 35, tzinfo=timezone.utc),
            schema_version="v0",  # only v1 supported
        )
