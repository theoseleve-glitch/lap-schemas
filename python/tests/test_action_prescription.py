from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.action_prescription import ActionPrescription
from lap_schemas.v1.environment import EnvironmentTag
from lap_schemas.v1.session_context import SessionContext
from lap_schemas.v1.success_condition import SuccessCondition


def _context() -> SessionContext:
    return SessionContext(
        car_id=uuid6.uuid7(),
        track_id=uuid6.uuid7(),
        track_layout="gp",
        environment_tag=EnvironmentTag.SIM_PRACTICE,
        conditions="dry, 22C",
    )


def _success() -> SuccessCondition:
    return SuccessCondition(
        metric="t1_trail_brake_release_pct",
        target_value=0.7,
        comparison="gte",
        target_pct=None,
        measurement_window="next_3_sessions",
    )


def test_action_prescription_accepts_proposed_prescription() -> None:
    pres = ActionPrescription(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        weakness_episode_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        priority="p1",
        due_before_session_id=None,
        valid_until=None,
        title="Trail-brake later into Spa T1",
        rationale="Your brake release is 15% too early; carrying pressure past turn-in recovers apex speed.",
        drill_template_id="drill.trail_brake.spa_t1",
        expected_context=_context(),
        success_condition=_success(),
        status="proposed",
        accepted_at=None,
        outcome_id=None,
    )
    assert pres.priority == "p1"
    assert pres.status == "proposed"
    assert pres.expected_context.track_layout == "gp"
    assert pres.success_condition.comparison == "gte"


def test_action_prescription_accepts_completed_with_outcome() -> None:
    outcome_id = uuid6.uuid7()
    pres = ActionPrescription(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        weakness_episode_id=None,  # standalone insight path
        created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
        priority="p0",
        due_before_session_id=uuid6.uuid7(),
        valid_until=datetime(2026, 4, 30, tzinfo=timezone.utc),
        title="Fix apex speed loss",
        rationale="Apex speed down 4 kph vs baseline.",
        drill_template_id=None,
        expected_context=_context(),
        success_condition=_success(),
        status="completed",
        accepted_at=datetime(2026, 4, 5, tzinfo=timezone.utc),
        outcome_id=outcome_id,
    )
    assert pres.weakness_episode_id is None
    assert pres.status == "completed"
    assert pres.outcome_id == outcome_id


def test_action_prescription_rejects_unknown_priority() -> None:
    with pytest.raises(ValidationError):
        ActionPrescription(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            weakness_episode_id=None,
            created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            priority="urgent",  # not in p0/p1/p2
            due_before_session_id=None,
            valid_until=None,
            title="x",
            rationale="y",
            drill_template_id=None,
            expected_context=_context(),
            success_condition=_success(),
            status="proposed",
            accepted_at=None,
            outcome_id=None,
        )
