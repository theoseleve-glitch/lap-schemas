"""T004 (sprint2-backend) — DriverProfileAggregate wrapper schema.

Composite response for `GET /api/v1/driver/profile`. Wraps the
four sections the client needs in a single round-trip:
- progress snapshot
- top-5 weakness episodes
- active prescriptions
- current readiness state

The wrapper uses `None` (not omitted fields) for sections the
driver hasn't accumulated yet, so clients can render placeholder
state from a fully-populated response shape.
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.action_prescription import ActionPrescriptionListItem
from lap_schemas.v1.driver_profile_aggregate import DriverProfileAggregate
from lap_schemas.v1.driver_progress_snapshot import DriverProgressSnapshot
from lap_schemas.v1.driver_readiness_state import DriverReadinessState
from lap_schemas.v1.skill_dimension import SkillDimension
from lap_schemas.v1.weakness_episode import WeaknessEpisode


def _skill() -> SkillDimension:
    return SkillDimension(
        score=70.0, confidence=0.8, trend_14d="flat", sample_count=10
    )


def _progress() -> DriverProgressSnapshot:
    return DriverProgressSnapshot(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        captured_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
        window="rolling_30d",
        window_start=datetime(2026, 3, 27, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 26, tzinfo=timezone.utc),
        braking=_skill(),
        throttle_pickup=_skill(),
        minimum_speed=_skill(),
        line_consistency=_skill(),
        tire_management=_skill(),
        racecraft=_skill(),
        fatigue_consistency=_skill(),
        strategy_execution=_skill(),
        setup_sensitivity=_skill(),
        adaptation=_skill(),
        overall_score=72.5,
        overall_confidence=0.85,
        generated_by="rules-v1",
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
        confidence=0.72,
        status="open",
        library_rule_id="rule.braking.late_release.v1",
    )


def _readiness() -> DriverReadinessState:
    return DriverReadinessState(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        computed_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
        readiness_score=68.0,
        volume_input=0.7,
        quality_input=0.8,
        recency_input=0.9,
        consistency_input=0.6,
        unresolved_weaknesses_input=0.5,
        familiarity_input=0.7,
        event_pressure_input=0.4,
        recovery_input=0.8,
        limiting_factor="line_consistency",
        likely_gain_area="braking",
        recommended_sessions_before_event=3,
    )


def _prescription() -> ActionPrescriptionListItem:
    return ActionPrescriptionListItem(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        weakness_episode_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
        priority="p0",
        title="Practice trail-braking",
        rationale="...",
        drill_template_id="drill.late_release.v1",
        success_condition={"comparison": "gte", "target_pct": 0.85},
        status="proposed",
    )


# -- shape ---------------------------------------------------------


def test_aggregate_round_trips_with_all_sections() -> None:
    payload = DriverProfileAggregate(
        progress=_progress(),
        top_weaknesses=[_weakness()],
        active_prescriptions=[_prescription()],
        readiness=_readiness(),
    )
    revived = DriverProfileAggregate.model_validate_json(
        payload.model_dump_json()
    )
    assert revived.progress is not None
    assert len(revived.top_weaknesses) == 1
    assert len(revived.active_prescriptions) == 1
    assert revived.readiness is not None


def test_aggregate_with_no_data_uses_nulls() -> None:
    """A new driver with no sessions yet should still get a
    well-shaped response — None for each missing section, empty
    lists for collections."""
    payload = DriverProfileAggregate(
        progress=None,
        top_weaknesses=[],
        active_prescriptions=[],
        readiness=None,
    )
    revived = DriverProfileAggregate.model_validate_json(
        payload.model_dump_json()
    )
    assert revived.progress is None
    assert revived.readiness is None
    assert list(revived.top_weaknesses) == []
    assert list(revived.active_prescriptions) == []


def test_top_weaknesses_capped_at_five() -> None:
    """Spec says top-5. Pin the cap so the wire shape can't grow
    silently — the client renders a fixed-height block."""
    six = [_weakness() for _ in range(6)]
    with pytest.raises(ValidationError):
        DriverProfileAggregate(
            progress=None,
            top_weaknesses=six,
            active_prescriptions=[],
            readiness=None,
        )


def test_aggregate_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        DriverProfileAggregate(  # type: ignore[call-arg]
            progress=None,
            top_weaknesses=[],
            active_prescriptions=[],
            readiness=None,
            unknown="oops",
        )
