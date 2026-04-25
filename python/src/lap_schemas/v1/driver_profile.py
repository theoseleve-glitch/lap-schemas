from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

SkillLevel = Literal["beginner", "intermediate", "advanced", "pro"]


class DriverProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    user_id: UUID7
    display_name: str = Field(min_length=1, max_length=128)
    skill_level: SkillLevel
    cohort_opt_in: bool


class DriverProfileUpdate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    display_name: str | None = Field(default=None, min_length=1, max_length=128)
    skill_level: SkillLevel | None = None
    cohort_opt_in: bool | None = None
