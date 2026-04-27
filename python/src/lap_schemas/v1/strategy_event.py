"""T099 — request + response shapes for runtime strategy events.

Backs POST /api/v1/sessions/{session_id}/strategy/events. Each
event is one append-only row in T097's StrategyEvent table —
the runtime story of what actually happened during the session
(plan set, alternate strategy armed, pit stop, stint end, FCY,
SC).

The request body omits id/session_id/created_at (server-sourced)
and driver_id entirely (implied by session ownership). `kind` is
a Literal of the spec set so a useful 422 surfaces on typos
instead of a CHECK-constraint reject. `details` is a free
dict[str, object] — the per-kind payload shape evolves faster
than the table schema.
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

StrategyEventKind = Literal[
    "plan", "armed", "pit", "stint_end", "fcy", "sc",
]


class StrategyEventCreate(BaseModel):
    """Request body. Bounds:
      - kind ∈ {plan, armed, pit, stint_end, fcy, sc} (Literal)
      - at_lap >= 0 (lap 0 = pre-grid; e.g., a `plan` event
        recorded before lap 1 sits at lap 0)
      - details defaults to {} so a kind-only event (e.g., "fcy"
        with no further metadata) can omit the field
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: StrategyEventKind
    at_lap: int = Field(ge=0)
    details: dict[str, Any] = Field(default_factory=dict)


class StrategyEvent(BaseModel):
    """Response. Mirrors the StrategyEvent ORM row 1:1 minus
    the driver_id (implied by session ownership)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    session_id: UUID7
    kind: StrategyEventKind
    at_lap: int
    details: dict[str, Any]
    created_at: datetime
