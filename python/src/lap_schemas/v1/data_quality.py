from pydantic import BaseModel, ConfigDict, Field


class DataQuality(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    score: float = Field(ge=0, le=100)
    gps_fix_quality: float | None = None
    gps_satellite_count_avg: int | None = None
    channel_completeness: float = Field(ge=0, le=100)
    sample_gaps_count: int = Field(ge=0)
    sample_rate_stability: float = Field(ge=0)
    warnings: tuple[str, ...] = Field(default_factory=tuple)
    recommendations: tuple[str, ...] = Field(default_factory=tuple)
    usable_for_overlays: bool
    usable_for_long_term_coaching: bool
