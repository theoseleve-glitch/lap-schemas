"""T009 (sprint2-backend) — drilldown view of a single skill dimension.

`GET /api/v1/driver/skills/{dimension}` returns a focused view of
one of the ten DriverProgressSnapshot dimensions. The wrapper
collapses three sources into one round-trip:

- ``current`` — the most recent SkillDimension reading (None if
  the driver has no progress snapshots yet, so a fresh-account
  drilldown still returns 200 with an empty payload instead of 404)
- ``trend`` — historical SkillTrendPoint samples for charting
- ``best_session`` / ``worst_session`` — SessionScoreRef pointers
  at the dimension's extremes (None if there's <1 historical
  reading to compare against)
- ``related_weaknesses`` — open WeaknessEpisode rows tagged to the
  domain category that maps to this dimension

The dimension name is restricted to the same ten dimensions
defined as fields on DriverProgressSnapshot — the Literal here is
the contract; the snapshot fields are the storage. Adding a new
dimension means updating both.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.skill_dimension import SkillDimension
from lap_schemas.v1.weakness_episode import WeaknessEpisode

SkillDimensionName = Literal[
    "braking",
    "throttle_pickup",
    "minimum_speed",
    "line_consistency",
    "tire_management",
    "racecraft",
    "fatigue_consistency",
    "strategy_execution",
    "setup_sensitivity",
    "adaptation",
]


class SkillTrendPoint(BaseModel):
    """One historical sample of a single dimension for charting."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    captured_at: datetime
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)


class SessionScoreRef(BaseModel):
    """Minimal pointer to a session, with the dimension score at that
    snapshot. Used for ``best_session`` / ``worst_session`` so the
    client can deep-link without fetching the full session."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    captured_at: datetime
    score: float = Field(ge=0, le=100)


class SkillDrilldown(BaseModel):
    """Composite response for the skill drilldown endpoint."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    dimension: SkillDimensionName
    current: SkillDimension | None = None
    trend: tuple[SkillTrendPoint, ...] = Field(default_factory=tuple)
    best_session: SessionScoreRef | None = None
    worst_session: SessionScoreRef | None = None
    related_weaknesses: tuple[WeaknessEpisode, ...] = Field(
        default_factory=tuple
    )
