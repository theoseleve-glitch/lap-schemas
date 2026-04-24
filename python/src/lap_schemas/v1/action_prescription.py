from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.session_context import SessionContext
from lap_schemas.v1.success_condition import SuccessCondition

PrescriptionPriority = Literal["p0", "p1", "p2"]
PrescriptionStatus = Literal[
    "proposed",
    "accepted",
    "in_progress",
    "completed",
    "skipped",
    "expired",
]


class ActionPrescription(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    weakness_episode_id: UUID7 | None = None
    created_at: datetime

    priority: PrescriptionPriority
    due_before_session_id: UUID7 | None = None
    valid_until: datetime | None = None

    title: str
    rationale: str
    drill_template_id: str | None = None
    expected_context: SessionContext
    success_condition: SuccessCondition

    status: PrescriptionStatus
    accepted_at: datetime | None = None
    outcome_id: UUID7 | None = None
