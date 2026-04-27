"""T171 — coach dashboard aggregate per-driver shape.

Backs `GET /api/v1/orgs/:org_id/dashboard` — a list-style endpoint
that returns one entry per driver in the org with enough info for
a dashboard table:

  - identity (user_id, display_name, skill_level)
  - latest progress signal (overall_score, last_progress_at)
  - active workload counts (open weaknesses, open prescriptions)

Why a lean per-driver shape and not the full DriverProfileAggregate
(T004)?
  - The dashboard is N drivers wide × table-row tall — tens of
    drivers, not one. Returning the full aggregate per row would
    inflate the payload and pull data the table doesn't render.
  - The aggregate is for a single-driver detail view; the
    dashboard is for the at-a-glance roster.

Empty / unset fields are valid:
  - A driver-role org member who hasn't created a DriverProfile
    yet has display_name=None, skill_level=None, overall_score=
    None, last_progress_at=None, but the row still appears
    (so the coach knows the driver exists). Counts default to 0.

`open_weaknesses` counts WeaknessEpisode rows in status ∈ {open,
improving} (matches `_OPEN_WEAKNESS_STATUSES` in skills.py).
`open_prescriptions` counts ActionPrescription rows in status
∈ {proposed, accepted, in_progress} (matches `_OPEN_RX_STATUSES`
in driver_profile.py).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.driver_profile import SkillLevel
from lap_schemas.v1.ids import UUID7


class CoachDashboardDriverEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: UUID7
    display_name: str | None = None
    skill_level: SkillLevel | None = None
    overall_score: float | None = None
    last_progress_at: datetime | None = None
    open_weaknesses: int = Field(ge=0, default=0)
    open_prescriptions: int = Field(ge=0, default=0)


class CoachDashboardResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: tuple[CoachDashboardDriverEntry, ...]
