"""T107 — driver-scoped strategy template CRUD shapes.

Backs `POST/GET/DELETE /api/v1/driver/strategy/templates`. The
template is a driver-saved StrategyPlan-shaped intent ("my Le
Mans strategy") that can be reused as the seed for many future
sessions' plans.

Distinct from T098's StrategyPlanCreate despite the identical
plan-shape fields:
  - StrategyPlanCreate is the per-session canonical plan (T096)
  - StrategyTemplateCreate is the per-driver named library entry

Bounds mirror StrategyPlanCreate so a client converting one to
the other never produces a payload the other side rejects:
  - planned_stints >= 1
  - planned_fuel_liters > 0
  - planned_pit_laps: list of lap numbers (1-indexed)

`name` is bounded [1, 120] chars: empty would be unnamable in
the UI list (reject at the boundary so the persisted set is
always discriminable); 120 matches the ORM column width.

Response omits driver_id — ownership is implied by the auth'd
caller.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class StrategyTemplateCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    planned_stints: int = Field(ge=1)
    planned_fuel_liters: float = Field(gt=0)
    planned_pit_laps: list[int] = Field(default_factory=list)


class StrategyTemplate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    created_at: datetime
    name: str
    planned_stints: int
    planned_fuel_liters: float
    planned_pit_laps: tuple[int, ...]


class StrategyTemplateList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: tuple[StrategyTemplate, ...]
