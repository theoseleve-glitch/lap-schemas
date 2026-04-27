"""T098 — request + response shapes for the pre-race strategy plan.

Backs POST /api/v1/sessions/{session_id}/strategy/plan (T098).
The request omits id/session_id/created_at — those are server-
sourced (id from UUID7, session_id from the path, created_at
from the server clock). Drops driver_id entirely: ownership is
derived from the authed user via the session's driver_id.

Why a single canonical shape (one plan per session): a re-plan
during the race is logged as a new StrategyEvent (T097) rather
than mutating this row, so the audit trail survives. The
endpoint returns 409 on duplicate so clients see the conflict
instead of silently overwriting.

planned_pit_laps is a tuple in the response and a list in the
request — frozen response per the established lap-schemas
pattern; lists in the request are clearer to clients building
JSON arrays. The runtime accepts either via Pydantic coercion.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class StrategyPlanCreate(BaseModel):
    """Request body. Bounds chosen for sim-realism:
      - planned_stints >= 1: a "0-stint plan" is meaningless
      - planned_fuel_liters > 0: a no-fuel plan can't run
      - planned_pit_laps entries >= 1: laps are 1-indexed in
        the rest of the codebase (Lap.lap_number is 1-indexed)
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    planned_stints: int = Field(ge=1)
    planned_fuel_liters: float = Field(gt=0)
    planned_pit_laps: list[int] = Field(default_factory=list)


class StrategyPlan(BaseModel):
    """Response. Mirrors the StrategyPlan ORM row 1:1 minus the
    driver_id (which is implied by ownership of the session)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    session_id: UUID7
    created_at: datetime
    planned_stints: int
    planned_fuel_liters: float
    planned_pit_laps: tuple[int, ...]
