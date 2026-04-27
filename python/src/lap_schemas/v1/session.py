from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.data_quality import DataQuality
from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.objective import ObjectiveTag
from lap_schemas.v1.sensor_config import SensorConfigSnapshot
from lap_schemas.v1.session_strategy_section import SessionStrategySection
from lap_schemas.v1.source import SourceTag

CaptureApp = Literal["lap-coach-logger", "lap-mobile-ios", "lap-mobile-android"]
RealHardware = Literal["racebox", "phone_only", "aim_solo", "vbox_sport"]
SessionStatus = Literal["uploaded", "processing", "ready", "failed"]


class SessionDetail(BaseModel):
    """Read model returned by GET /api/v1/sessions/{session_id} (T123).

    Lightweight summary the UI/SSE consumers poll while a session
    moves through processing. The rich post-processing payload lives
    on the related `SessionRecord` row, exposed separately.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    status: SessionStatus
    created_at: datetime
    failure_reason: str | None = None


class SessionManifest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    driver_id: UUID7
    bundle_version: Literal["v2"]

    capture_app: CaptureApp
    capture_app_version: str
    device_model: str
    device_os: str
    device_os_version: str

    source: SourceTag
    sim_title: str | None = None
    real_hardware: RealHardware | None = None

    car_id: UUID7
    track_id: UUID7
    track_layout: str
    environment_tag: EnvironmentTag
    objective_tag: ObjectiveTag | None = None
    training_block_id: UUID7 | None = None
    endurance_event_id: UUID7 | None = None
    strategy_section: SessionStrategySection | None = None

    started_at: datetime
    ended_at: datetime
    duration_seconds: float = Field(ge=0)

    telemetry_checksums: dict[str, str]
    total_samples: int = Field(ge=0)
    sample_rate_hz: float = Field(gt=0)

    data_quality: DataQuality
    sensor_config: SensorConfigSnapshot
