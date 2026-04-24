from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DivergenceType = Literal["shape", "intensity", "both"]


class DivergencePoint(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    track_distance_m: float = Field(ge=0)
    metric: str
    sim_value: float
    real_value: float
    divergence_type: DivergenceType
