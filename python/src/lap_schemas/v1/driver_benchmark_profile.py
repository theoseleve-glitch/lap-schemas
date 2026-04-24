from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.ids import UUID7

DriverArchetype = Literal[
    "late_braker",
    "smooth_flow",
    "aggressive_exit",
    "consistent_executor",
    "adaptive_racecraft",
]


class CohortDef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    skill_level: str | None = None
    car_class: str | None = None
    track_id: UUID7 | None = None
    environment_tag: EnvironmentTag | None = None
    min_sessions: int = Field(default=5, ge=0)


class DriverBenchmarkProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    generated_at: datetime

    cohort_definition: CohortDef
    cohort_size: int = Field(ge=0)

    per_track_car_percentiles: dict[str, float] = Field(default_factory=dict)
    per_dimension_percentiles: dict[str, float] = Field(default_factory=dict)

    archetype: DriverArchetype | None = None
