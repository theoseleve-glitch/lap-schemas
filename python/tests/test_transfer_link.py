from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.divergence_point import DivergencePoint
from lap_schemas.v1.transfer_link import TransferLink


def test_transfer_link_accepts_auto_pairing() -> None:
    link = TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="same_track",
        shape_match_score=0.82,
        intensity_match_score=0.74,
        divergence_points=(),
        transferred_skills=("braking", "line_consistency"),
        non_transferred_skills=(),
        generated_report_id=None,
    )
    assert link.created_by == "auto"
    assert link.link_reason == "same_track"
    assert link.transferred_skills == ("braking", "line_consistency")
    assert link.generated_report_id is None


def test_transfer_link_accepts_manual_pairing_with_divergences() -> None:
    report_id = uuid6.uuid7()
    dp = DivergencePoint(
        track_distance_m=312.5,
        metric="brake_pressure_peak",
        sim_value=0.9,
        real_value=0.65,
        divergence_type="intensity",
    )
    link = TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        created_by="user",
        session_pair=(uuid6.uuid7(), uuid6.uuid7(), uuid6.uuid7()),
        link_reason="manual",
        shape_match_score=0.55,
        intensity_match_score=0.40,
        divergence_points=(dp,),
        transferred_skills=("minimum_speed",),
        non_transferred_skills=("braking",),
        generated_report_id=report_id,
    )
    assert link.created_by == "user"
    assert len(link.divergence_points) == 1
    assert link.divergence_points[0].divergence_type == "intensity"
    assert link.generated_report_id == report_id


def test_transfer_link_rejects_unknown_link_reason() -> None:
    with pytest.raises(ValidationError):
        TransferLink(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            created_by="auto",
            session_pair=(uuid6.uuid7(), uuid6.uuid7()),
            link_reason="vibe_based",  # not in allowed set
            shape_match_score=0.5,
            intensity_match_score=0.5,
            divergence_points=(),
            transferred_skills=(),
            non_transferred_skills=(),
            generated_report_id=None,
        )


# -- T016 (sprint2-backend): round-trip + import surface ----------


def test_transfer_link_round_trip_json() -> None:
    """T016 acceptance: a TransferLink survives a full
    model_dump_json → model_validate_json cycle without losing
    any field. This is the wire-contract pin for the bridge
    entity (ADR-005 §5.5)."""
    original = TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="event_prep",
        shape_match_score=0.91,
        intensity_match_score=0.83,
        divergence_points=(
            DivergencePoint(
                track_distance_m=120.0,
                metric="brake_pressure_peak",
                sim_value=0.8,
                real_value=0.6,
                divergence_type="intensity",
            ),
        ),
        transferred_skills=("braking",),
        non_transferred_skills=("minimum_speed",),
        generated_report_id=uuid6.uuid7(),
    )
    revived = TransferLink.model_validate_json(original.model_dump_json())
    assert revived == original


def test_transfer_link_session_pair_requires_at_least_two() -> None:
    """Per ADR-005 §5.5 a TransferLink represents a *pair* (or
    multi-set, usually 2) of comparable sessions. A single-session
    'pair' has no comparison to make and shouldn't validate."""
    with pytest.raises(ValidationError):
        TransferLink(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            created_by="auto",
            session_pair=(uuid6.uuid7(),),  # only 1 — rejected
            link_reason="same_track",
            shape_match_score=0.5,
            intensity_match_score=0.5,
            divergence_points=(),
            transferred_skills=(),
            non_transferred_skills=(),
            generated_report_id=None,
        )


def test_transfer_link_re_exported_from_v1_root() -> None:
    """Consumers should be able to `from lap_schemas.v1 import
    TransferLink, DivergencePoint` without reaching into module
    paths — same convention as other v1 schemas."""
    from lap_schemas.v1 import (
        DivergencePoint as _DP,
    )
    from lap_schemas.v1 import (
        TransferLink as _TL,
    )

    assert _TL is TransferLink
    assert _DP is DivergencePoint


# -- T019 (sprint2-backend): TransferLinkCreate request shape -----


def test_transfer_link_create_minimal_payload() -> None:
    """Request shape for `POST /api/v1/bridge/links`. id, driver_id,
    and created_at are server-set (not client-provided), so the
    create wrapper omits them. Defaults match TransferLink for the
    optional list-typed fields."""
    from lap_schemas.v1.transfer_link import TransferLinkCreate

    req = TransferLinkCreate(
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="same_track",
        shape_match_score=0.78,
        intensity_match_score=0.62,
    )
    assert req.divergence_points == ()
    assert req.transferred_skills == ()
    assert req.non_transferred_skills == ()
    assert req.generated_report_id is None


def test_transfer_link_create_session_pair_requires_at_least_two() -> None:
    from lap_schemas.v1.transfer_link import TransferLinkCreate

    with pytest.raises(ValidationError):
        TransferLinkCreate(
            created_by="user",
            session_pair=(uuid6.uuid7(),),
            link_reason="manual",
            shape_match_score=0.5,
            intensity_match_score=0.5,
        )


def test_transfer_link_create_round_trip_json() -> None:
    from lap_schemas.v1.transfer_link import TransferLinkCreate

    original = TransferLinkCreate(
        created_by="user",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="manual",
        shape_match_score=0.5,
        intensity_match_score=0.5,
        divergence_points=(
            DivergencePoint(
                track_distance_m=100.0,
                metric="brake_pressure_peak",
                sim_value=0.5,
                real_value=0.7,
                divergence_type="intensity",
            ),
        ),
        transferred_skills=("braking",),
    )
    revived = TransferLinkCreate.model_validate_json(original.model_dump_json())
    assert revived == original


def test_transfer_link_create_re_exported_from_v1_root() -> None:
    from lap_schemas.v1 import TransferLinkCreate as _TLC
    from lap_schemas.v1.transfer_link import TransferLinkCreate

    assert _TLC is TransferLinkCreate


# -- T021 (sprint2-backend): TransferLinkList paginated wrapper ---


def _link() -> TransferLink:
    return TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="same_track",
        shape_match_score=0.78,
        intensity_match_score=0.62,
    )


def test_transfer_link_list_round_trip_json() -> None:
    """Paginated wrapper for `GET /api/v1/driver/:id/bridge/links`.
    Same shape as TrackCatalogList so the web app can reuse its
    pagination component."""
    from lap_schemas.v1.transfer_link import TransferLinkList

    page = TransferLinkList(
        items=(_link(), _link()),
        total=2,
        limit=20,
        offset=0,
    )
    revived = TransferLinkList.model_validate_json(page.model_dump_json())
    assert revived == page


def test_transfer_link_list_empty_page_is_valid() -> None:
    from lap_schemas.v1.transfer_link import TransferLinkList

    page = TransferLinkList(items=(), total=0, limit=20, offset=0)
    assert page.items == ()
    assert page.total == 0


def test_transfer_link_list_limit_must_be_positive() -> None:
    from lap_schemas.v1.transfer_link import TransferLinkList

    with pytest.raises(ValidationError):
        TransferLinkList(items=(), total=0, limit=0, offset=0)


def test_transfer_link_list_re_exported_from_v1_root() -> None:
    from lap_schemas.v1 import TransferLinkList as _TLL
    from lap_schemas.v1.transfer_link import TransferLinkList

    assert _TLL is TransferLinkList


# -- T023 (sprint2-backend): rating shape -------------------------


def test_transfer_link_rating_defaults_unrated() -> None:
    """A freshly created link has no usefulness rating yet — both
    usefulness_rating and rated_at default to None so the POST T019
    payload doesn't have to pass them."""
    link = TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="same_track",
        shape_match_score=0.7,
        intensity_match_score=0.6,
    )
    assert link.usefulness_rating is None
    assert link.rated_at is None


def test_transfer_link_accepts_thumbs_up() -> None:
    rated = TransferLink(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
        created_by="auto",
        session_pair=(uuid6.uuid7(), uuid6.uuid7()),
        link_reason="same_track",
        shape_match_score=0.7,
        intensity_match_score=0.6,
        usefulness_rating="up",
        rated_at=datetime(2026, 4, 25, 12, tzinfo=timezone.utc),
    )
    assert rated.usefulness_rating == "up"


def test_transfer_link_rejects_unknown_rating() -> None:
    with pytest.raises(ValidationError):
        TransferLink(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            created_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
            created_by="auto",
            session_pair=(uuid6.uuid7(), uuid6.uuid7()),
            link_reason="same_track",
            shape_match_score=0.7,
            intensity_match_score=0.6,
            usefulness_rating="meh",  # not in allowed set
        )


def test_bridge_link_rating_request_round_trip() -> None:
    from lap_schemas.v1.transfer_link import BridgeLinkRatingRequest

    body = BridgeLinkRatingRequest(rating="down")
    revived = BridgeLinkRatingRequest.model_validate_json(body.model_dump_json())
    assert revived.rating == "down"


def test_bridge_link_rating_request_rejects_unknown_rating() -> None:
    from lap_schemas.v1.transfer_link import BridgeLinkRatingRequest

    with pytest.raises(ValidationError):
        BridgeLinkRatingRequest(rating="okay")  # type: ignore[arg-type]


def test_bridge_link_rating_request_re_exported_from_v1_root() -> None:
    from lap_schemas.v1 import BridgeLinkRatingRequest as _R
    from lap_schemas.v1.transfer_link import BridgeLinkRatingRequest

    assert _R is BridgeLinkRatingRequest
