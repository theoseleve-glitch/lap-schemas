"""T106 — driver-scoped strategy history list response.

`GET /api/v1/driver/strategy/history` returns the authenticated
driver's recent sessions that have a StrategyPlan (T096) attached,
each entry carrying the plan summary and the persisted T102
execution_score. Powers the webapp's "your strategy history"
view so drivers can see how plan-vs-actual execution is trending
session over session.

Each entry exposes the plan summary fields plus the score; the
detailed timeline / divergence / visualization for one entry
lives on the per-session endpoints (T100/T105) — kept off the
list to avoid N+1 event queries on every load.

execution_score is `int | None`: `None` = "not yet finalized"
(distinct from `0` = "catastrophic divergence"). The list still
includes None entries so in-flight sessions appear in the
chronological view.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7


class StrategyHistoryEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    session_created_at: datetime
    planned_stints: int
    planned_fuel_liters: float
    planned_pit_laps: tuple[int, ...]
    execution_score: int | None


class StrategyHistoryList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: tuple[StrategyHistoryEntry, ...]
