"""T103 — `strategy_section` shape carried inside SessionManifest.

A bundle-time declaration of the pre-race plan: the capture
client records the driver's intent at the moment the bundle is
sealed, so the server can bootstrap T096's StrategyPlan row at
ingest time without a follow-up POST round-trip.

Distinct from T098's `StrategyPlanCreate` despite the identical
field set:
  - `StrategyPlanCreate` is the API request body for the
    mutable runtime POST endpoint (clients can re-plan during
    the race; conflicts return 409).
  - `SessionStrategySection` lives inside the immutable
    SessionManifest, so it's part of the bundle's tamper-
    evident snapshot. Future fields (notes, source-of-plan
    metadata, sim-vs-real flags) belong here, not on the API
    body — keeping them as separate models lets each side
    evolve without coupling the bundle wire format to the
    runtime API surface.

Field bounds match StrategyPlanCreate so a client converting one
to the other never produces a payload the other side rejects.
"""

from pydantic import BaseModel, ConfigDict, Field


class SessionStrategySection(BaseModel):
    """Pre-race plan declared inside a v2 bundle manifest.

    Bounds mirror StrategyPlanCreate:
      - planned_stints >= 1
      - planned_fuel_liters > 0
      - planned_pit_laps: list of 1-indexed lap numbers
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    planned_stints: int = Field(ge=1)
    planned_fuel_liters: float = Field(gt=0)
    planned_pit_laps: list[int] = Field(default_factory=list)
