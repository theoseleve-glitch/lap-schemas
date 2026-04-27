"""T100 — combined plan + actual timeline response.

Backs GET /api/v1/sessions/{session_id}/strategy/timeline. The
response is the full strategy story for one session: the
canonical pre-race plan (T096) plus the runtime event log
(T097) ordered by lap. The UI renders the two side-by-side so
the driver can see "intended pit at 25 / actual pit at 22"
during a debrief.

Why a wrapper object instead of returning the bare list of
events: future-additions safety. Adding a `plan_revision_count`
or a `derived_metrics` field later is a non-breaking field
add to a wrapper; on a top-level array it would force a v2
endpoint.

`plan` is None when the driver never set a pre-race plan —
distinct from "set but had every field zeroed". The UI shows
"no plan recorded" vs "plan was empty" differently.
"""

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.strategy_event import StrategyEvent
from lap_schemas.v1.strategy_plan import StrategyPlan


class StrategyTimelineResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    plan: StrategyPlan | None
    events: tuple[StrategyEvent, ...]
