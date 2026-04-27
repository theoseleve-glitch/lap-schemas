"""T105 — webapp-facing aggregated read for plan-vs-actual chart.

Backs GET /api/v1/sessions/{session_id}/strategy/visualization.
Bundles T096's StrategyPlan, the actual pit/fuel/stint outcomes
derived from T097's StrategyEvent timeline, and T102's persisted
execution_score in a single round trip — the webapp draws the
chart without three sequential calls or rebuilding the
event-to-actuals math client-side.

Why a separate model vs reusing StrategyTimelineResponse (T100):
  - StrategyTimelineResponse returns the raw (plan, events) for
    any consumer that wants the full event stream.
  - StrategyVisualization returns visualization-shaped aggregates:
    pit-laps as a sorted tuple, fuel summed, stint lengths
    derived. The webapp consumes shapes ready for chart axes,
    keeping the matching math (fuel summing, stint-length
    derivation) on the server where it can stay aligned with
    T101's divergence math.

`actual_pit_laps` is sorted ASC (chart x-axis).
`actual_fuel_liters_total` mirrors T101's defensive
`details.get("fuel_added_liters", 0)` — tire-only stops
legitimately omit the key and contribute 0.
`actual_stint_lengths` is derived from stint_end events:
stint 1 = first end_lap; stint N = end_lap[N] - end_lap[N-1].
`execution_score` is None until T102 finalization — distinct
from "score is 0" (catastrophic divergence).
"""

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.strategy_plan import StrategyPlan


class StrategyVisualization(BaseModel):
    """Aggregated read for the webapp's plan-vs-actual chart."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    plan: StrategyPlan | None
    actual_pit_laps: tuple[int, ...]
    actual_fuel_liters_total: float
    actual_stint_lengths: tuple[int, ...]
    execution_score: int | None
