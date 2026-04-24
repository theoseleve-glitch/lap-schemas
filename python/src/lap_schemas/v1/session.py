from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.data_quality import DataQuality
from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.objective import ObjectiveTag
from lap_schemas.v1.sensor_config import SensorConfigSnapshot
from lap_schemas.v1.source import SourceTag

CaptureApp = Literal["lap-coach-logger", "lap-mobile-ios", "lap-mobile-android"]
RealHardware = Literal["racebox", "phone_only", "aim_solo", "vbox_sport"]


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

    started_at: datetime
    ended_at: datetime
    duration_seconds: float = Field(ge=0)

    telemetry_checksums: dict[str, str]
    total_samples: int = Field(ge=0)
    sample_rate_hz: float = Field(gt=0)

    data_quality: DataQuality
    sensor_config: SensorConfigSnapshot
