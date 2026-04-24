from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.coaching_insight import CoachingInsight


def test_coaching_insight_accepts_per_session_finding() -> None:
    insight = CoachingInsight(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        rule_id="br.late_braking.apex_speed_loss",
        rule_version="1.2.0",
        observation="Apex speed 4 kph below your rolling average across Spa T1.",
        evidence=("brake_release_pct=0.62 vs target 0.80", "apex_speed=38.2 mps"),
        likely_cause="Braking 10m earlier than needed.",
        severity="medium",
        confidence=0.78,
        corner_tag="Spa/T1",
        suggested_prescription_id=uuid6.uuid7(),
        flagged_false_positive=False,
    )
    assert insight.rule_id == "br.late_braking.apex_speed_loss"
    assert insight.rule_version == "1.2.0"
    assert len(insight.evidence) == 2
    assert insight.severity == "medium"
    assert insight.suggested_prescription_id is not None


def test_coaching_insight_accepts_flagged_false_positive() -> None:
    insight = CoachingInsight(
        id=uuid6.uuid7(),
        session_id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        rule_id="br.abrupt_release.load_transfer_mismatch",
        rule_version="1.0.0",
        observation="Detected load transfer mismatch at T2.",
        evidence=(),
        likely_cause=None,
        severity="low",
        confidence=0.41,
        corner_tag=None,
        suggested_prescription_id=None,
        flagged_false_positive=True,
    )
    assert insight.flagged_false_positive is True
    assert insight.likely_cause is None
    assert insight.corner_tag is None
    assert insight.evidence == ()


def test_coaching_insight_rejects_unknown_severity() -> None:
    with pytest.raises(ValidationError):
        CoachingInsight(
            id=uuid6.uuid7(),
            session_id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            created_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            rule_id="x",
            rule_version="1",
            observation="y",
            evidence=(),
            likely_cause=None,
            severity="critical",  # must be low/medium/high
            confidence=0.5,
            corner_tag=None,
            suggested_prescription_id=None,
            flagged_false_positive=False,
        )
