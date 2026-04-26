from datetime import datetime, timezone

import uuid6

from lap_schemas.v1.data_quality import DataQuality
from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.objective import ObjectiveTag
from lap_schemas.v1.sensor_config import SensorConfig, SensorConfigSnapshot
from lap_schemas.v1.session import SessionManifest


def _minimal_quality() -> DataQuality:
    return DataQuality(
        score=95.0,
        channel_completeness=100.0,
        sample_gaps_count=0,
        sample_rate_stability=0.0,
        usable_for_overlays=True,
        usable_for_long_term_coaching=True,
    )


def test_session_manifest_accepts_sim_session() -> None:
    manifest = SessionManifest(
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
        objective_tag=ObjectiveTag.DRILL,
        training_block_id=None,
        started_at=datetime(2026, 4, 24, 10, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 10, 45, tzinfo=timezone.utc),
        duration_seconds=2700.0,
        telemetry_checksums={"samples.bin": "sha256:abc"},
        total_samples=120000,
        sample_rate_hz=60.0,
        data_quality=_minimal_quality(),
        sensor_config=SensorConfigSnapshot(
            sensors=(SensorConfig(name="irsdk", sample_rate_hz=60.0),),
        ),
    )
    assert manifest.source == "iracing"
    assert manifest.sim_title == "iracing"
    assert manifest.real_hardware is None
    assert manifest.environment_tag is EnvironmentTag.SIM_PRACTICE
    assert manifest.objective_tag is ObjectiveTag.DRILL


def test_session_manifest_accepts_real_session() -> None:
    manifest = SessionManifest(
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        bundle_version="v2",
        capture_app="lap-mobile-ios",
        capture_app_version="1.0.0",
        device_model="iPhone 15",
        device_os="iOS",
        device_os_version="18.0",
        source="real",
        sim_title=None,
        real_hardware="racebox",
        car_id=uuid6.uuid7(),
        track_id=uuid6.uuid7(),
        track_layout="long",
        environment_tag=EnvironmentTag.REAL_TRACK_DAY,
        objective_tag=None,
        training_block_id=None,
        started_at=datetime(2026, 4, 24, 9, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 10, 30, tzinfo=timezone.utc),
        duration_seconds=5400.0,
        telemetry_checksums={"gnss.bin": "sha256:def", "imu.bin": "sha256:123"},
        total_samples=90000,
        sample_rate_hz=10.0,
        data_quality=_minimal_quality(),
        sensor_config=SensorConfigSnapshot(),
    )
    assert manifest.source == "real"
    assert manifest.sim_title is None
    assert manifest.real_hardware == "racebox"
    assert manifest.objective_tag is None


def test_session_manifest_endurance_event_id_defaults_to_none() -> None:
    """T066 (sprint2-backend) — `endurance_event_id` is server-set
    after ingest correlates a session to an EnduranceEvent (T067).
    Capture clients never produce it, so the field MUST default to
    None when omitted. Pin the additive-non-breaking shape: existing
    clients keep validating without changes."""
    manifest = SessionManifest(
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
        objective_tag=ObjectiveTag.DRILL,
        training_block_id=None,
        started_at=datetime(2026, 4, 24, 10, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 10, 45, tzinfo=timezone.utc),
        duration_seconds=2700.0,
        telemetry_checksums={"samples.bin": "sha256:abc"},
        total_samples=120000,
        sample_rate_hz=60.0,
        data_quality=_minimal_quality(),
        sensor_config=SensorConfigSnapshot(),
    )
    assert manifest.endurance_event_id is None


def test_session_manifest_accepts_endurance_event_id_and_round_trips() -> None:
    """T066 (sprint2-backend) — when a session belongs to an endurance
    event, the field carries the event id (UUID7) and survives a JSON
    round-trip unchanged. Mutation: dropping the field from the model
    or losing it on serialization would lose the link to T067's
    EnduranceEvent and break the long-run scoring pipeline."""
    event_id = uuid6.uuid7()
    original = SessionManifest(
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        bundle_version="v2",
        capture_app="lap-coach-logger",
        capture_app_version="0.9.0",
        device_model="Desktop",
        device_os="Linux",
        device_os_version="6.1",
        source="iracing",
        sim_title="iracing",
        real_hardware=None,
        car_id=uuid6.uuid7(),
        track_id=uuid6.uuid7(),
        track_layout="gp",
        environment_tag=EnvironmentTag.SIM_RACE,
        objective_tag=ObjectiveTag.RACE_PREP,
        training_block_id=None,
        endurance_event_id=event_id,
        started_at=datetime(2026, 4, 24, 18, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 22, 0, tzinfo=timezone.utc),
        duration_seconds=14400.0,
        telemetry_checksums={"samples.bin": "sha256:xyz"},
        total_samples=864000,
        sample_rate_hz=60.0,
        data_quality=_minimal_quality(),
        sensor_config=SensorConfigSnapshot(),
    )
    assert original.endurance_event_id == event_id
    encoded = original.model_dump_json()
    reloaded = SessionManifest.model_validate_json(encoded)
    assert reloaded.endurance_event_id == event_id
    assert reloaded == original


def test_session_manifest_json_roundtrip() -> None:
    original = SessionManifest(
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        bundle_version="v2",
        capture_app="lap-coach-logger",
        capture_app_version="0.9.0",
        device_model="Desktop",
        device_os="Linux",
        device_os_version="6.1",
        source="acc",
        sim_title="acc",
        real_hardware=None,
        car_id=uuid6.uuid7(),
        track_id=uuid6.uuid7(),
        track_layout="gp",
        environment_tag=EnvironmentTag.SIM_RACE,
        objective_tag=ObjectiveTag.RACE_PREP,
        training_block_id=uuid6.uuid7(),
        started_at=datetime(2026, 4, 24, 18, 0, tzinfo=timezone.utc),
        ended_at=datetime(2026, 4, 24, 19, 0, tzinfo=timezone.utc),
        duration_seconds=3600.0,
        telemetry_checksums={"samples.bin": "sha256:xyz"},
        total_samples=216000,
        sample_rate_hz=60.0,
        data_quality=_minimal_quality(),
        sensor_config=SensorConfigSnapshot(
            sensors=(SensorConfig(name="acc_shmem", sample_rate_hz=60.0),),
        ),
    )
    encoded = original.model_dump_json()
    reloaded = SessionManifest.model_validate_json(encoded)
    assert reloaded == original
