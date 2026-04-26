"""T046 (sprint2-backend) — bridge suggest-links response.

Response schema for GET /api/v1/bridge/suggest_links?session_id=X.
Given one of the driver's sessions, return other sessions that
could plausibly pair with it for bridge analysis (same master
track, same car class, recent).

The candidate carries enough metadata for the UI to render a
choose-your-pair list — id and creation timestamp. Track/car
metadata is intentionally not duplicated here; the UI hydrates
that detail from the session list.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7


class BridgeSuggestLinkCandidate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: UUID7
    created_at: datetime


class BridgeSuggestLinkList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_session_id: UUID7
    candidates: tuple[BridgeSuggestLinkCandidate, ...]
