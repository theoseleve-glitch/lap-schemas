"""T093 — response shape for GET /api/v1/driver/target-events/countdown.

Server-side countdown to the driver's soonest UPCOMING TargetEvent.
Why server-side instead of client-computed:
  - server clock is authoritative; client clocks drift, especially
    on mobile where countdown precision matters in the final hours
  - the same endpoint can fold in derived helpers (days/hours
    rounded) so the UI doesn't need to ship date-math twice
  - `server_now` is echoed so the client can warn on local-clock
    drift (a cosmetic 30-min skew is harmless; a 12-hour skew
    means a different "today" and warrants a UI hint)

Shape:
  - target_event: the soonest TargetEvent with starts_at >= now,
    or None when the driver has no upcoming pin
  - seconds_until_start / days_until_start: convenience deltas;
    both None when target_event is None (no event, no countdown)
  - server_now: server-stamped at endpoint time, RFC3339 UTC

Past pins are excluded by design — the countdown view is forward-
looking. T085's calendar feed and T084's list endpoint are the
right places to surface "events you've already done".
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.driver_readiness_state import TargetEvent


class TargetEventCountdown(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    target_event: TargetEvent | None
    seconds_until_start: int | None = Field(default=None, ge=0)
    days_until_start: int | None = Field(default=None, ge=0)
    server_now: datetime
