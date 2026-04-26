"""T005 (sprint2-backend) — saved A/B compare case schemas.

A CompareCase is a driver-saved comparison between two or more
sessions, with a free-text rationale ("why was Spa slower last
week?"). Persisted so the user can revisit the comparison
later — and so an outcome block can re-evaluate when the
referenced sessions reprocess (T006).

`CompareCaseCreate` is the POST input. `CompareCase` is the
returned/persisted shape.
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


class CompareCase(BaseModel):
    """Persisted compare case as returned by GET / POST."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    session_ids: tuple[UUID7, ...] = Field(min_length=2, max_length=10)
    rationale: str = Field(min_length=1, max_length=_RATIONALE_MAX_LEN)
    created_at: datetime
