"""T009 (sprint2-backend) — SkillDrilldown wrapper schema.

Composite response for `GET /api/v1/driver/skills/{dimension}`.
Wraps a single skill dimension with:
- current: most-recent SkillDimension reading
- trend: time-ordered SkillTrendPoint history for charting
- best_session / worst_session: SessionScoreRef pointers at extremes
- related_weaknesses: open WeaknessEpisode rows tagged to this
  dimension's domain category

Each sidecar defaults to empty/None so a freshly-tracked dimension
with no history yet still serializes cleanly.
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.skill_dimension import SkillDimension
from lap_schemas.v1.skill_drilldown import (
    SessionScoreRef,
    SkillDrilldown,
    SkillTrendPoint,
)
from lap_schemas.v1.weakness_episode import WeaknessEpisode


def _dim() -> SkillDimension:
    return SkillDimension(
        score=72.5,
        confidence=0.8,
        trend_14d="up",
        last_evidence_session_id=uuid6.uuid7(),
        sample_count=12,
    )


def _trend_point() -> SkillTrendPoint:
    return SkillTrendPoint(
        captured_at=datetime(2026, 4, 20, tzinfo=timezone.utc),
        score=68.0,
        confidence=0.7,
    )


def _session_ref() -> SessionScoreRef:
    return SessionScoreRef(
        session_id=uuid6.uuid7(),
        captured_at=datetime(2026, 4, 22, tzinfo=timezone.utc),
        score=80.0,
    )


def _weakness() -> WeaknessEpisode:
    return WeaknessEpisode(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        category="technique",
        subcategory="late_release",
        first_observed_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
        last_observed_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
        recurrence_count=4,
        severity="medium",
        confidence=0.7,
        status="open",
        library_rule_id="rule.x.v1",
    )


# -- SkillTrendPoint -----------------------------------------------


def test_trend_point_round_trip() -> None:
    p = _trend_point()
    revived = SkillTrendPoint.model_validate_json(p.model_dump_json())
    assert revived == p


def test_trend_point_score_must_be_in_range() -> None:
    with pytest.raises(ValidationError):
        SkillTrendPoint(
            captured_at=datetime.now(timezone.utc),
            score=120.0,
            confidence=0.5,
        )


def test_trend_point_confidence_must_be_in_range() -> None:
    with pytest.raises(ValidationError):
        SkillTrendPoint(
            captured_at=datetime.now(timezone.utc),
            score=50.0,
            confidence=1.5,
        )


def test_trend_point_rejects_extras() -> None:
    with pytest.raises(ValidationError):
        SkillTrendPoint(  # type: ignore[call-arg]
            captured_at=datetime.now(timezone.utc),
            score=50.0,
            confidence=0.5,
            unknown="x",
        )


# -- SessionScoreRef -----------------------------------------------


def test_session_ref_round_trip() -> None:
    r = _session_ref()
    revived = SessionScoreRef.model_validate_json(r.model_dump_json())
    assert revived == r


def test_session_ref_score_must_be_in_range() -> None:
    with pytest.raises(ValidationError):
        SessionScoreRef(
            session_id=uuid6.uuid7(),
            captured_at=datetime.now(timezone.utc),
            score=-1.0,
        )


# -- SkillDrilldown ------------------------------------------------


def test_drilldown_minimal_payload() -> None:
    d = SkillDrilldown(dimension="braking", current=_dim())
    assert d.trend == ()
    assert d.best_session is None
    assert d.worst_session is None
    assert d.related_weaknesses == ()


def test_drilldown_with_all_sections() -> None:
    d = SkillDrilldown(
        dimension="braking",
        current=_dim(),
        trend=(_trend_point(), _trend_point()),
        best_session=_session_ref(),
        worst_session=_session_ref(),
        related_weaknesses=(_weakness(),),
    )
    revived = SkillDrilldown.model_validate_json(d.model_dump_json())
    assert revived.dimension == "braking"
    assert len(revived.trend) == 2
    assert revived.best_session is not None
    assert revived.worst_session is not None
    assert len(revived.related_weaknesses) == 1


def test_drilldown_dimension_must_be_known() -> None:
    with pytest.raises(ValidationError):
        SkillDrilldown(
            dimension="not_a_dimension",  # type: ignore[arg-type]
            current=_dim(),
        )


def test_drilldown_accepts_each_known_dimension() -> None:
    for name in (
        "braking",
        "throttle_pickup",
        "minimum_speed",
        "line_consistency",
        "tire_management",
        "racecraft",
        "fatigue_consistency",
        "strategy_execution",
        "setup_sensitivity",
        "adaptation",
    ):
        SkillDrilldown(dimension=name, current=_dim())  # type: ignore[arg-type]


def test_drilldown_rejects_extras() -> None:
    with pytest.raises(ValidationError):
        SkillDrilldown(  # type: ignore[call-arg]
            dimension="braking",
            current=_dim(),
            unknown="oops",
        )
