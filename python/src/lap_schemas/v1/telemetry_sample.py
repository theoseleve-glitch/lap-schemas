from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SourceClock = Literal[
    "gnss",
    "coremotion",
    "racebox_gnss",
    "irsdk_tick",
    "acc_shmem",
    "device_monotonic",
]


class TelemetrySample(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    t_source_ns: int = Field(ge=0)
    t_canonical_ns: int = Field(ge=0)
    t_source_clock: SourceClock
    channels: dict[str, float] = Field(default_factory=dict)
