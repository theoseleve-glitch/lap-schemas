"""T076 (sprint2-backend) — driver endurance history list response.

`GET /api/v1/driver/endurance/history` returns the EnduranceEvents
the authenticated driver is entered in. Membership comes from the
EnduranceEvent.driver_ids roster (T067) — explicit, not session-
derived — so pre-event entries appear in the list before any
session has been logged.

Each entry exposes only the planned-shape fields (id, event_name,
total_duration_seconds, stint_count). Recorded aggregates live on
the per-event T075 summary endpoint to keep the list response
small and avoid N+1 stint queries.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class DriverEnduranceHistoryEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    event_name: str
    total_duration_seconds: float = Field(ge=0)
    stint_count: int = Field(ge=0)


class DriverEnduranceHistoryList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    events: tuple[DriverEnduranceHistoryEntry, ...]
