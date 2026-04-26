from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.divergence_point import DivergencePoint
from lap_schemas.v1.ids import UUID7

TransferCreatedBy = Literal["user", "auto"]
TransferLinkReason = Literal["same_track", "event_prep", "similar_car_class", "manual"]
# T023 (sprint2-backend) — driver feedback on a link's usefulness.
# Two-state thumbs feedback rather than a 1-5 star: easier UI, and
# the only operational use we have for ratings is "is this rule
# producing useful suggestions" — a binary signal is enough.
BridgeLinkRating = Literal["up", "down"]


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

    # T023 (sprint2-backend) — driver feedback. Both default to None
    # so existing TransferLink construction sites (and the T019 POST
    # body) don't have to pass them. `rated_at` lets us answer "how
    # fresh is this signal?" when aggregating rule health.
    usefulness_rating: BridgeLinkRating | None = None
    rated_at: datetime | None = None

    # T029 (sprint2-backend) — link lifecycle. Server stamps
    # `stale_at` when a session referenced in `session_pair` is
    # deleted. Once stamped it stays — re-marking is a no-op and
    # we never automatically un-stale a link (the missing session
    # isn't coming back). Consumers can filter `stale_at IS NULL`
    # or surface a "session no longer available" badge.
    stale_at: datetime | None = None


class TransferLinkList(BaseModel):
    """Paginated wrapper for `GET /api/v1/driver/:id/bridge/links`
    (T021). Same shape as TrackCatalogList so the web app can
    reuse its pagination component."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    items: tuple[TransferLink, ...]
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)


class TransferLinkCreate(BaseModel):
    """Request body for `POST /api/v1/bridge/links` (T019).

    Mirrors `TransferLink` minus the server-controlled fields:
    `id` (server-generated UUID7), `driver_id` (derived from auth),
    and `created_at` (server clock). Everything else is client-
    supplied — including `created_by` so the caller declares
    whether the link was a user-issued manual pairing or an
    auto-detected suggestion they accepted.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    created_by: TransferCreatedBy
    session_pair: tuple[UUID7, ...] = Field(min_length=2)
    link_reason: TransferLinkReason

    shape_match_score: float = Field(ge=0, le=1)
    intensity_match_score: float = Field(ge=0, le=1)
    divergence_points: tuple[DivergencePoint, ...] = Field(default_factory=tuple)

    transferred_skills: tuple[str, ...] = Field(default_factory=tuple)
    non_transferred_skills: tuple[str, ...] = Field(default_factory=tuple)

    generated_report_id: UUID7 | None = None


class BridgeLinkRatingRequest(BaseModel):
    """Request body for `POST /api/v1/bridge/links/:id/rate` (T023).

    Single-field POST: the driver's thumbs-up/down on whether this
    link's analysis was actually useful. The endpoint stamps
    `rated_at` server-side, so callers only send the rating itself.
    Re-rating overwrites — there's only one rating per link.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    rating: BridgeLinkRating
