"""T058 (sprint2-backend) — driver benchmark response.

`GET /api/v1/driver/benchmark?car_id=...&track_id=...` returns
the authenticated driver's percentile in the cohort for the
requested (car, track) context.

`percentiles` is intentionally typed `dict[str, float] | None`:
  - None → the cohort has not unlocked (per ADR-008, <20 distinct
    opted-in drivers). Clients display "Cohort unlocks at 20
    comparable drivers." (per ADR-008 messaging).
  - dict (possibly empty) → cohort is unlocked. Each key is a
    skill dimension name; value is the driver's percentile rank
    in [0, 1]. Missing dimensions → no cohort data for that
    (car, track, metric); client should treat as "no rank".
"""

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7


class DriverBenchmarkResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    car_id: UUID7
    track_id: UUID7
    percentiles: dict[str, float] | None = None
