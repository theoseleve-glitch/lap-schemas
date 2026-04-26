from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7
from lap_schemas.v1.skill_dimension import SkillDimension

ProgressWindow = Literal["session", "week", "month", "rolling_30d"]


class DriverProgressSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    captured_at: datetime
    window: ProgressWindow
    window_start: datetime
    window_end: datetime

    braking: SkillDimension
    throttle_pickup: SkillDimension
    minimum_speed: SkillDimension
    line_consistency: SkillDimension
    tire_management: SkillDimension
    racecraft: SkillDimension
    fatigue_consistency: SkillDimension
    strategy_execution: SkillDimension
    setup_sensitivity: SkillDimension
    adaptation: SkillDimension

    # T073 endurance-weighted dimensions. Optional because sprint-only
    # drivers won't have stint-level data; default None preserves the
    # additive non-breaking shape for every existing snapshot.
    long_run_consistency: SkillDimension | None = None
    pace_decay: SkillDimension | None = None
    tire_preservation: SkillDimension | None = None

    overall_score: float = Field(ge=0, le=100)
    overall_confidence: float = Field(ge=0, le=1)
    percentile_vs_cohort: float | None = Field(default=None, ge=0, le=1)

    generated_by: str
