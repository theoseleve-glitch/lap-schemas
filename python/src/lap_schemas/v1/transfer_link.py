from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.divergence_point import DivergencePoint
from lap_schemas.v1.ids import UUID7

TransferCreatedBy = Literal["user", "auto"]
TransferLinkReason = Literal["same_track", "event_prep", "similar_car_class", "manual"]


class TransferLink(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    driver_id: UUID7
    created_at: datetime
    created_by: TransferCreatedBy

    # Per ADR-005 §5.5 a link is a *pair* (or multi-set) of
    # comparable sessions — usually 2, never 1. A single-session
    # link has no comparison to make.
    session_pair: tuple[UUID7, ...] = Field(min_length=2)
    link_reason: TransferLinkReason

    shape_match_score: float = Field(ge=0, le=1)
    intensity_match_score: float = Field(ge=0, le=1)
    divergence_points: tuple[DivergencePoint, ...] = Field(default_factory=tuple)

    transferred_skills: tuple[str, ...] = Field(default_factory=tuple)
    non_transferred_skills: tuple[str, ...] = Field(default_factory=tuple)

    generated_report_id: UUID7 | None = None
