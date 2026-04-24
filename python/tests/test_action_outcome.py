from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.action_outcome import ActionOutcome


def test_action_outcome_accepts_success() -> None:
    out = ActionOutcome(
        id=uuid6.uuid7(),
        prescription_id=uuid6.uuid7(),
        measured_at=datetime(2026, 4, 24, 18, 30, tzinfo=timezone.utc),
        session_ids_measured=(uuid6.uuid7(), uuid6.uuid7()),
        success_condition_met=True,
        measured_value=0.82,
        delta_vs_baseline=0.18,
        confidence_change=0.25,
        prescription_efficacy_score=0.87,
        notes=None,
    )
    assert out.success_condition_met is True
    assert out.delta_vs_baseline == 0.18
    assert out.prescription_efficacy_score == 0.87


def test_action_outcome_accepts_failure_with_negative_delta() -> None:
    out = ActionOutcome(
        id=uuid6.uuid7(),
        prescription_id=uuid6.uuid7(),
        measured_at=datetime(2026, 4, 24, 18, 30, tzinfo=timezone.utc),
        session_ids_measured=(uuid6.uuid7(),),
        success_condition_met=False,
        measured_value=0.61,
        delta_vs_baseline=-0.04,  # regression
        confidence_change=-0.10,  # episode confidence grew
        prescription_efficacy_score=0.12,
        notes="Driver reported being unwell during session — re-prescribe after rest.",
    )
    assert out.success_condition_met is False
    assert out.delta_vs_baseline < 0
    assert out.confidence_change < 0
    assert out.notes is not None


def test_action_outcome_rejects_efficacy_score_above_one() -> None:
    with pytest.raises(ValidationError):
        ActionOutcome(
            id=uuid6.uuid7(),
            prescription_id=uuid6.uuid7(),
            measured_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            session_ids_measured=(),
            success_condition_met=True,
            measured_value=1.0,
            delta_vs_baseline=1.0,
            confidence_change=0.5,
            prescription_efficacy_score=1.5,  # bound is 0-1 per ADR-005 §5.4
            notes=None,
        )
