from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.driver_readiness_state import (
    DriverReadinessState,
    TargetEvent,
)


def _event() -> TargetEvent:
    return TargetEvent(
        id=uuid6.uuid7(),
        name="iRacing Rolex 24 Special Event",
        kind="sim_event",
        starts_at=datetime(2026, 5, 20, 14, 0, tzinfo=timezone.utc),
        ends_at=datetime(2026, 5, 21, 14, 0, tzinfo=timezone.utc),
        track_id=uuid6.uuid7(),
        car_id=uuid6.uuid7(),
        competitive_weight=0.8,
        notes=None,
    )


def test_target_event_accepts_sim_event() -> None:
    event = _event()
    assert event.kind == "sim_event"
    assert event.competitive_weight == 0.8
    assert event.notes is None


def test_driver_readiness_state_accepts_all_ten_inputs() -> None:
    state = DriverReadinessState(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        target_event=_event(),
        computed_at=datetime(2026, 5, 1, tzinfo=timezone.utc),
        readiness_score=72.5,
        volume_input=0.80,
        quality_input=0.90,
        recency_input=0.70,
        consistency_input=0.65,
        unresolved_weaknesses_input=0.50,
        familiarity_input=0.55,
        event_pressure_input=0.80,
        recovery_input=0.90,
        limiting_factor="unresolved_weaknesses_input",
        likely_gain_area="braking",
        recommended_sessions_before_event=3,
    )
    assert state.readiness_score == 72.5
    assert state.limiting_factor == "unresolved_weaknesses_input"
    assert state.recommended_sessions_before_event == 3
    assert state.target_event is not None
    assert state.target_event.kind == "sim_event"


def test_driver_readiness_state_rejects_readiness_score_above_100() -> None:
    with pytest.raises(ValidationError):
        DriverReadinessState(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            target_event=None,
            computed_at=datetime(2026, 5, 1, tzinfo=timezone.utc),
            readiness_score=150.0,  # bound is 0-100
            volume_input=0.5,
            quality_input=0.5,
            recency_input=0.5,
            consistency_input=0.5,
            unresolved_weaknesses_input=0.5,
            familiarity_input=0.5,
            event_pressure_input=0.5,
            recovery_input=0.5,
            limiting_factor="volume_input",
            likely_gain_area="consistency",
            recommended_sessions_before_event=0,
        )
