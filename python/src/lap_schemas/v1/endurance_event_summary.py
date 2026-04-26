"""T075 (sprint2-backend) — endurance event summary response.

`GET /api/v1/endurance/events/{event_id}` returns a roll-up of the
event metadata (planned shape from the EnduranceEvent row, T067)
plus aggregates derived from sessions linked via
SessionManifest.endurance_event_id (T066) and their StintRecords
(T069).

Aggregates default to None when no stints have been recorded —
clients distinguish "event scheduled but nothing logged yet" from
a real 0.0 (which would be perfect-preservation pace decay).
Coercing to 0.0 would mis-render the early-state UI.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class EnduranceEventSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Planned shape (from EnduranceEvent row, T067)
    id: UUID7
    event_name: str
    total_duration_seconds: float = Field(ge=0)
    stint_count: int = Field(ge=0)
    driver_ids: list[UUID7]

    # Recorded aggregates (from sessions + stint_records)
    recorded_session_count: int = Field(ge=0)
    recorded_stint_count: int = Field(ge=0)
    mean_lap_time_decay_seconds: float | None = None
    mean_fuel_used_liters: float | None = None
