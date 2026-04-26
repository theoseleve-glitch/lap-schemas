"""T007 (sprint2-backend) — weakness detail wrapper.

`GET /api/v1/driver/weaknesses/{id}` returns the WeaknessEpisode
plus three resolved sidecars:
- history: per-session timeline derived from
  WeaknessEpisode.sessions_affected (so the client doesn't need
  a separate /sessions/{id} round-trip per row to render dates)
- evidence: CoachingInsight rows whose ids appear in
  WeaknessEpisode.linked_insights
- linked_prescriptions: ActionPrescriptionListItem rows whose
  ids appear in WeaknessEpisode.linked_prescriptions

Each sidecar defaults to empty so a freshly-detected episode
with no evidence/prescriptions yet still serializes cleanly.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.coaching_insight import CoachingInsight
from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.weakness_episode import WeaknessEpisode


class WeaknessHistoryEntry(BaseModel):
    """One entry in the weakness's per-session history."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    session_created_at: datetime


class WeaknessDetail(BaseModel):
    """Composite response for the weakness detail endpoint."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    weakness: WeaknessEpisode
    history: list[WeaknessHistoryEntry] = Field(default_factory=list)
    evidence: list[CoachingInsight] = Field(default_factory=list)
    linked_prescriptions: list[ActionPrescriptionListItem] = Field(
        default_factory=list
    )
