"""T084 — GET /api/v1/driver/target-events list response.

Wrapper around tuple[TargetEvent, ...] for the driver-scoped pin
list. Frozen tuple matches the established list pattern (see
endurance_history.py): immutability prevents accidental mutation
in clients that hold the response, and tuple is JSON-array-
serialized just like list — no over-the-wire change vs list[].

Why a wrapper object instead of a bare top-level array: top-level
JSON arrays prevent backwards-compatible field additions (you'd
need a v2 schema). With `target_events: [...]`, we can later add
`next_cursor`, `total_count`, etc. without breaking clients.
"""

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.driver_readiness_state import TargetEvent


class TargetEventList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    target_events: tuple[TargetEvent, ...]
