from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

TargetEventKind = Literal["sim_event", "real_track_day", "real_race", "real_test"]


class TargetEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    name: str
    kind: TargetEventKind
    starts_at: datetime
    ends_at: datetime | None = None
    track_id: UUID7 | None = None
    car_id: UUID7 | None = None
    competitive_weight: float = Field(ge=0, le=1)
    notes: str | None = None


class DriverReadinessState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    target_event: TargetEvent | None = None
    computed_at: datetime

    readiness_score: float = Field(ge=0, le=100)

    volume_input: float
    quality_input: float
    recency_input: float
    consistency_input: float
    unresolved_weaknesses_input: float
    familiarity_input: float
    event_pressure_input: float
    recovery_input: float

    limiting_factor: str
    likely_gain_area: str
    recommended_sessions_before_event: int = Field(ge=0)
