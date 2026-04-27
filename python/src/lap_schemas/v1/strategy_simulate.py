"""T109 — strategy simulation request + response shapes.

Backs `POST /api/v1/sessions/{session_id}/strategy/simulate`.
"What if I pitted 2 laps later?" — given an actual session with
its event log already recorded, the endpoint scores a
hypothetical alternate plan against the same actual events. The
caller submits a hypothetical plan + total_race_laps and gets
back T101's divergence deltas + T102's execution score.

Distinct from T098's StrategyPlanCreate despite carrying the
same plan-shape fields:
  - StrategyPlanCreate is the canonical per-session POST that
    persists the row and returns the StrategyPlan response
  - StrategySimulateRequest is the read-only what-if request
    that adds `total_race_laps` (StrategyPlan doesn't carry
    race length on its row — total_race_laps is the simulator's
    extra context)

Field bounds mirror StrategyPlanCreate so a client converting one
to the other never produces a payload the other side rejects.
`total_race_laps > 0`: the divergence math has no race scaffold
without it; rejecting at the boundary catches typos before T101
short-circuits to all-zeros.

Response shape mirrors T101's StrategyDivergence dataclass plus
T102's int-bounded execution_score. Score is always int (T102
clamps and rounds), never None — simulation always produces a
score because the "actual" inputs are present.
"""

from pydantic import BaseModel, ConfigDict, Field


class StrategySimulateRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    planned_stints: int = Field(ge=1)
    planned_fuel_liters: float = Field(gt=0)
    planned_pit_laps: list[int] = Field(default_factory=list)
    total_race_laps: int = Field(gt=0)


class StrategySimulateResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pit_lap_delta_total: int
    fuel_delta_liters: float
    stint_duration_delta_laps: int
    execution_score: int
