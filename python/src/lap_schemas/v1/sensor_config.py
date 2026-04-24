from pydantic import BaseModel, ConfigDict, Field


class SensorConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    sample_rate_hz: float = Field(gt=0)
    enabled: bool = True


class SensorConfigSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sensors: tuple[SensorConfig, ...] = Field(default_factory=tuple)
    hardware_id: str | None = None
    firmware_version: str | None = None
