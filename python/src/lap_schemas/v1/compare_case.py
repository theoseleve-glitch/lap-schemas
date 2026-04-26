"""T005/T006 (sprint2-backend) — saved A/B compare case schemas.

A CompareCase is a driver-saved comparison between two or more
sessions, with a free-text rationale ("why was Spa slower last
week?"). Persisted so the user can revisit the comparison
later — and so an outcome block can re-evaluate when the
referenced sessions reprocess (T006).

`CompareCaseCreate` is the POST input.
`CompareCase` is the persisted/returned shape; the optional
`sessions` field carries a per-session snapshot (T006) populated
by GET only — POST returns it as None.
`CompareCaseSessionSnapshot` is one row of the snapshot block.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

_RATIONALE_MAX_LEN = 2000


class CompareCaseCreate(BaseModel):
    """POST /api/v1/compare_cases input."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_ids: tuple[UUID7, ...] = Field(min_length=2, max_length=10)
    rationale: str = Field(min_length=1, max_length=_RATIONALE_MAX_LEN)


class CompareCaseSessionSnapshot(BaseModel):
    """Per-session live snapshot included in GET responses (T006).

    Fields are optional because a referenced session may not have
    a SessionRecord yet (still processing). Clients render
    "still processing" for nulls rather than choking."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    processed_at: datetime | None = None
    best_lap_ms: int | None = Field(default=None, ge=0)
    total_laps: int | None = Field(default=None, ge=0)
    valid_laps: int | None = Field(default=None, ge=0)


class CompareCase(BaseModel):
    """Persisted compare case as returned by GET / POST.

    `sessions` is None on POST (no snapshot to compute at create
    time) and populated on GET with a fresh per-session snapshot
    so reprocesses are reflected without manual cache busting.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    session_ids: tuple[UUID7, ...] = Field(min_length=2, max_length=10)
    rationale: str = Field(min_length=1, max_length=_RATIONALE_MAX_LEN)
    created_at: datetime
    sessions: tuple[CompareCaseSessionSnapshot, ...] | None = None
