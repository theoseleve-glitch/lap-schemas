"""T007 (sprint2-backend) — WeaknessDetail wrapper schema.

Composite response for `GET /api/v1/driver/weaknesses/{id}`.
Wraps the episode with three resolved sidecars:
- history: per-session presence timeline derived from
  WeaknessEpisode.sessions_affected
- evidence: CoachingInsight rows linked to this episode
- linked_prescriptions: ActionPrescriptionListItem rows
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.coaching_insight import CoachingInsight
from lap_schemas.v1.weakness_detail import (
    WeaknessDetail,
    WeaknessHistoryEntry,
)
from lap_schemas.v1.weakness_episode import WeaknessEpisode


def _ep() -> WeaknessEpisode:
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


def _hist() -> WeaknessHistoryEntry:
    return WeaknessHistoryEntry(
        session_id=uuid6.uuid7(),
        session_created_at=datetime(2026, 4, 20, tzinfo=timezone.utc),
    )


def _insight() -> CoachingInsight:
    return CoachingInsight(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 20, tzinfo=timezone.utc),
        rule_id="rule.x.v1",
        rule_version="1",
        observation="late release",
        severity="medium",
        confidence=0.8,
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


def test_history_entry_round_trip() -> None:
    h = _hist()
    revived = WeaknessHistoryEntry.model_validate_json(h.model_dump_json())
    assert revived == h


def test_history_entry_rejects_extras() -> None:
    with pytest.raises(ValidationError):
        WeaknessHistoryEntry(  # type: ignore[call-arg]
            session_id=uuid6.uuid7(),
            session_created_at=datetime.now(timezone.utc),
            unknown="x",
        )


def test_detail_with_all_sections() -> None:
    detail = WeaknessDetail(
        weakness=_ep(),
        history=[_hist(), _hist()],
        evidence=[_insight()],
        linked_prescriptions=[_rx()],
    )
    revived = WeaknessDetail.model_validate_json(detail.model_dump_json())
    assert len(revived.history) == 2
    assert len(revived.evidence) == 1
    assert len(revived.linked_prescriptions) == 1


def test_detail_empty_sidecars_default() -> None:
    detail = WeaknessDetail(weakness=_ep())
    assert list(detail.history) == []
    assert list(detail.evidence) == []
    assert list(detail.linked_prescriptions) == []


def test_detail_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        WeaknessDetail(  # type: ignore[call-arg]
            weakness=_ep(),
            unknown="oops",
        )
