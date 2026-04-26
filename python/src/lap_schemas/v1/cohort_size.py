"""T059 (sprint2-backend) — cohort size response.

`GET /api/v1/driver/cohort_size?car_id=...&track_id=...` returns
the current count of opted-in drivers in the cohort, plus the
unlock threshold. UI uses this for the "17 / 20 drivers" progress
display when DriverBenchmarkResponse.percentiles is null.

unlock_threshold is server-controlled (vs. UI hardcoded) so a
future ADR-008 update to k=15 or k=25 doesn't strand the UI on
a stale constant.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class CohortSizeResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    car_id: UUID7
    track_id: UUID7
    cohort_size: int = Field(ge=0)
    unlock_threshold: int = Field(ge=0)
