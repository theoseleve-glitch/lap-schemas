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
