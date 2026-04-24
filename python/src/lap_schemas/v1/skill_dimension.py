from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

Trend14d = Literal["up", "flat", "down", "volatile"]


class SkillDimension(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    trend_14d: Trend14d
    last_evidence_session_id: UUID7 | None = None
    sample_count: int = Field(ge=0)
