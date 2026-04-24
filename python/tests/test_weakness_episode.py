from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.weakness_category import WeaknessCategory
from lap_schemas.v1.weakness_episode import WeaknessEpisode


def test_weakness_episode_accepts_open_episode() -> None:
    ep = WeaknessEpisode(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        category=WeaknessCategory.TECHNIQUE,
        subcategory="late_braking",
        corner_tag="Spa/T1",
        environment_scope=(EnvironmentTag.SIM_PRACTICE, EnvironmentTag.REAL_TRACK_DAY),
        first_observed_at=datetime(2026, 3, 1, tzinfo=timezone.utc),
        last_observed_at=datetime(2026, 4, 20, tzinfo=timezone.utc),
        recurrence_count=12,
        sessions_affected=(uuid6.uuid7(), uuid6.uuid7()),
        severity="medium",
        confidence=0.74,
        status="open",
        resolved_at=None,
        linked_prescriptions=(uuid6.uuid7(),),
        linked_insights=(uuid6.uuid7(), uuid6.uuid7()),
        library_rule_id="br.late_braking.apex_speed_loss",
    )
    assert ep.category is WeaknessCategory.TECHNIQUE
    assert ep.status == "open"
    assert ep.resolved_at is None
    # Default confidence decay per ADR-005 §5.2 is 0.02.
    assert ep.confidence_decay_per_day == 0.02


def test_weakness_episode_accepts_resolved_without_corner() -> None:
    ep = WeaknessEpisode(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        category=WeaknessCategory.CONSISTENCY,
        subcategory="lap_time_variance",
        corner_tag=None,
        environment_scope=(EnvironmentTag.SIM_RACE,),
        first_observed_at=datetime(2026, 1, 15, tzinfo=timezone.utc),
        last_observed_at=datetime(2026, 3, 10, tzinfo=timezone.utc),
        recurrence_count=4,
        sessions_affected=(),
        severity="low",
        confidence=0.25,
        confidence_decay_per_day=0.05,
        status="resolved",
        resolved_at=datetime(2026, 3, 10, tzinfo=timezone.utc),
        linked_prescriptions=(),
        linked_insights=(),
        library_rule_id="cs.lap_time_variance.sector_analysis",
    )
    assert ep.corner_tag is None
    assert ep.status == "resolved"
    assert ep.resolved_at == datetime(2026, 3, 10, tzinfo=timezone.utc)


def test_weakness_episode_rejects_sessions_affected_over_cap_of_fifty() -> None:
    too_many = tuple(uuid6.uuid7() for _ in range(51))
    with pytest.raises(ValidationError):
        WeaknessEpisode(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            category=WeaknessCategory.EXECUTION,
            subcategory="missed_apex",
            corner_tag=None,
            environment_scope=(),
            first_observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            last_observed_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
            recurrence_count=51,
            sessions_affected=too_many,
            severity="high",
            confidence=0.9,
            status="open",
            resolved_at=None,
            linked_prescriptions=(),
            linked_insights=(),
            library_rule_id="ex.missed_apex.generic",
        )
