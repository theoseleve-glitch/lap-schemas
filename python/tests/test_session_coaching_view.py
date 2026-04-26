"""T010 (sprint2-backend) — SessionCoachingView wrapper schema.

Composite response for `GET /api/v1/sessions/{id}/coaching`.
Aggregates everything a driver sees on the post-session coaching
review screen:
- insights: CoachingInsight rows the rules engine produced for
  this session
- weaknesses_touched: WeaknessEpisode rows linked back from those
  insights (the deeper "this is a recurring pattern" entities)
- prescriptions_generated: ActionPrescriptionListItem rows whose
  ids match `insight.suggested_prescription_id`

Each sidecar defaults to empty so a session with no coaching
findings still serializes cleanly (200, not 404).
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.coaching_insight import CoachingInsight
from lap_schemas.v1.session_coaching_view import SessionCoachingView
from lap_schemas.v1.weakness_episode import WeaknessEpisode


def _insight() -> CoachingInsight:
    return CoachingInsight(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 25, tzinfo=timezone.utc),
        rule_id="rule.x.v1",
        rule_version="1",
        observation="late release",
        severity="medium",
        confidence=0.8,
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


def _rx() -> ActionPrescriptionListItem:
    return ActionPrescriptionListItem(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        weakness_episode_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
        priority="p0",
        title="Practice trail-braking",
        rationale="...",
        drill_template_id="drill.x.v1",
        success_condition={"comparison": "gte", "target_pct": 0.85},
        status="proposed",
    )


def test_view_minimal_session_id_only() -> None:
    sid = uuid6.uuid7()
    v = SessionCoachingView(session_id=sid)
    assert v.session_id == sid
    assert v.insights == ()
    assert v.weaknesses_touched == ()
    assert v.prescriptions_generated == ()


def test_view_with_all_sections() -> None:
    v = SessionCoachingView(
        session_id=uuid6.uuid7(),
        insights=(_insight(), _insight()),
        weaknesses_touched=(_weakness(),),
        prescriptions_generated=(_rx(),),
    )
    revived = SessionCoachingView.model_validate_json(v.model_dump_json())
    assert len(revived.insights) == 2
    assert len(revived.weaknesses_touched) == 1
    assert len(revived.prescriptions_generated) == 1


def test_view_round_trip_preserves_session_id() -> None:
    sid = uuid6.uuid7()
    v = SessionCoachingView(session_id=sid)
    revived = SessionCoachingView.model_validate_json(v.model_dump_json())
    assert revived.session_id == sid


def test_view_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        SessionCoachingView(  # type: ignore[call-arg]
            session_id=uuid6.uuid7(),
            unknown="oops",
        )


def test_view_session_id_required() -> None:
    with pytest.raises(ValidationError):
        SessionCoachingView()  # type: ignore[call-arg]
