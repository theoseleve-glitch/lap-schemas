"""T172 — coach manual prescription create shape.

Backs `POST /api/v1/coach/prescriptions` — a coach (or org admin)
assigns a prescription to a driver in their org. Distinct from
the system-generated path: no `weakness_episode_id` because the
coach is acting on judgment rather than a triggered episode, and
`expected_context` / `success_condition` aren't required because
the coach reviews the outcome manually.

Bounds:
  - `title` ∈ [1, 256]: rejects empty (would render as a blank
    drill in the driver UI) and matches the ORM column width
  - `rationale` non-empty: a coach-assigned drill without a
    rationale gives the driver no actionable context. The whole
    point of a coach prescribing (over the system) is the
    explanation
  - `priority` ∈ {p0, p1, p2}: same closed-set as the system
    path; the schema layer is the boundary, not the DB
  - `drill_template_id` is optional — coaches frequently invent
    custom drills outside the catalog
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.action_prescription import PrescriptionPriority
from lap_schemas.v1.ids import UUID7


class CoachPrescriptionCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    org_id: UUID7
    driver_user_id: UUID7
    priority: PrescriptionPriority
    title: str = Field(min_length=1, max_length=256)
    rationale: str = Field(min_length=1)
    drill_template_id: str | None = Field(default=None, max_length=128)
