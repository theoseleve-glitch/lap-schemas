import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.skill_dimension import SkillDimension


def test_skill_dimension_accepts_fully_scored_dimension() -> None:
    dim = SkillDimension(
        score=72.5,
        confidence=0.83,
        trend_14d="up",
        last_evidence_session_id=uuid6.uuid7(),
        sample_count=14,
    )
    assert dim.score == 72.5
    assert dim.confidence == 0.83
    assert dim.trend_14d == "up"
    assert dim.sample_count == 14


def test_skill_dimension_accepts_cold_start_without_evidence() -> None:
    dim = SkillDimension(
        score=0.0,
        confidence=0.0,
        trend_14d="flat",
        last_evidence_session_id=None,
        sample_count=0,
    )
    assert dim.last_evidence_session_id is None
    assert dim.sample_count == 0


def test_skill_dimension_rejects_unknown_trend() -> None:
    with pytest.raises(ValidationError):
        SkillDimension(
            score=50.0,
            confidence=0.5,
            trend_14d="improving",  # not in allowed set
            last_evidence_session_id=None,
            sample_count=1,
        )
