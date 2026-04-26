"""T004 (sprint2-backend) — DriverProfileAggregate.

Composite response for `GET /api/v1/driver/profile`. One round-
trip surfaces all four sections a driver-home view needs:

- progress    — latest DriverProgressSnapshot (None if no sessions yet)
- top_weaknesses — up to 5 WeaknessEpisode rows ordered by severity
                   then recency; capped at 5 so the wire shape can't
                   grow silently and the client renders a fixed block
- active_prescriptions — ActionPrescriptionListItem rows in open
                         statuses (proposed / accepted / in_progress)
- readiness   — latest DriverReadinessState (None if no event set)

The wrapper uses None-not-omitted for missing sections so
clients can render placeholder state from a fully-populated
response shape.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.driver_progress_snapshot import DriverProgressSnapshot
from lap_schemas.v1.driver_readiness_state import DriverReadinessState
from lap_schemas.v1.weakness_episode import WeaknessEpisode


class DriverProfileAggregate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    progress: DriverProgressSnapshot | None = None
    top_weaknesses: list[WeaknessEpisode] = Field(
        default_factory=list, max_length=5
    )
    active_prescriptions: list[ActionPrescriptionListItem] = Field(
        default_factory=list
    )
    readiness: DriverReadinessState | None = None
