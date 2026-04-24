from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class ActionOutcome(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    prescription_id: UUID7
    measured_at: datetime
    session_ids_measured: tuple[UUID7, ...] = Field(default_factory=tuple)

    success_condition_met: bool
    measured_value: float
    delta_vs_baseline: float

    confidence_change: float
    prescription_efficacy_score: float = Field(ge=0, le=1)

    notes: str | None = None
