"""T010 (sprint2-backend) — aggregated coaching view for one session.

`GET /api/v1/sessions/{id}/coaching` collapses three coaching
sources into one round-trip:

- ``insights`` — every CoachingInsight the rules engine produced
  for this session
- ``weaknesses_touched`` — WeaknessEpisode rows whose
  ``linked_insights`` reference any insight in this session.
  These are the deeper "this is recurring" entities the session's
  observations contributed evidence to.
- ``prescriptions_generated`` — ActionPrescriptionListItem rows
  whose id appears as ``insight.suggested_prescription_id`` for
  any insight in this session

Each sidecar defaults to empty so a session that didn't trigger
any coaching findings still serializes cleanly (200, not 404).

Distinct from `next_actions` (T224): that endpoint surfaces
*open* prescriptions for the driver's next session; this one
surfaces what the rules engine *actually said* about the just-
completed session, including resolved/skipped artifacts.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.coaching_insight import CoachingInsight
from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.weakness_episode import WeaknessEpisode


class SessionCoachingView(BaseModel):
    """Composite response for the per-session coaching endpoint."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    insights: tuple[CoachingInsight, ...] = Field(default_factory=tuple)
    weaknesses_touched: tuple[WeaknessEpisode, ...] = Field(
        default_factory=tuple
    )
    prescriptions_generated: tuple[ActionPrescriptionListItem, ...] = Field(
        default_factory=tuple
    )
