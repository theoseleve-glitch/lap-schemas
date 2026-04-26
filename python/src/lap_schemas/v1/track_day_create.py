"""T088 — request body for POST /api/v1/driver/track-days.

UX-friendly form for manually-curated real-life events (private
track days, club races, regional series) where the venue isn't
in our iRacing-sourced catalog yet. Internally creates a
TargetEvent with kind="real_track_day" — the API surfaces a
"track day" verb the user understands, while the persistence
layer keeps a single TargetEvent table.

Why distinct from POST /target-events: that endpoint requires
the caller to set `kind` to a Literal string and to either
supply track_id (catalog FK) or leave it None. The UX is
target-event-modeling, not "I'm doing a track day Saturday."
This endpoint defaults `kind`, takes a free-text venue_name in
place of the catalog FK, and lets `competitive_weight` default
to 0.3 (track days are skill-building, not full-stakes).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrackDayCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    venue_name: str = Field(min_length=1, max_length=255)
    starts_at: datetime
    ends_at: datetime | None = None
    # Default 0.3: track days are skill-building, not full-stakes.
    # Caller can override toward 1.0 for an A-list club race.
    competitive_weight: float = Field(default=0.3, ge=0, le=1)
    notes: str | None = None
