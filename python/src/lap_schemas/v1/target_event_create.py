"""T082 — request body for POST /api/v1/driver/target-events.

`TargetEventCreate` is the client-supplied subset of `TargetEvent`
(see driver_readiness_state.py). Drops:
  - `id` — server-generated UUID7 to prevent client-supplied
    collision attempts and to guarantee uuid6.uuid7 monotonicity
    for downstream sort-by-creation queries.
  - `driver_id` — the request is auth-scoped; deriving from the
    bearer token closes the IDOR vector where one driver pins a
    target on another driver's profile.

Field constraints mirror `TargetEvent` so the persisted shape
matches what the client just sent (404 on round-trip would be a
schema-drift bug, not a contract change).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.driver_readiness_state import TargetEventKind
from lap_schemas.v1.ids import UUID7


class TargetEventCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    kind: TargetEventKind
    starts_at: datetime
    ends_at: datetime | None = None
    track_id: UUID7 | None = None
    car_id: UUID7 | None = None
    competitive_weight: float = Field(ge=0, le=1)
    notes: str | None = None
