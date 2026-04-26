from datetime import datetime, timedelta, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.driver_progress_snapshot import DriverProgressSnapshot
from lap_schemas.v1.skill_dimension import SkillDimension


def _dim(score: float, confidence: float = 0.8, samples: int = 12) -> SkillDimension:
    return SkillDimension(
        score=score,
        confidence=confidence,
        trend_14d="flat",
        last_evidence_session_id=uuid6.uuid7(),
        sample_count=samples,
    )


def example_snapshot() -> DriverProgressSnapshot:
    """Reusable example fixture per ADR-005 §5.1."""
    now = datetime(2026, 4, 24, 12, 0, tzinfo=timezone.utc)
    return DriverProgressSnapshot(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        captured_at=now,
        window="rolling_30d",
        window_start=now - timedelta(days=30),
        window_end=now,
        braking=_dim(74.0),
        throttle_pickup=_dim(68.5),
        minimum_speed=_dim(71.0),
        line_consistency=_dim(66.0),
        tire_management=_dim(60.0, confidence=0.5, samples=4),
        racecraft=_dim(55.0, confidence=0.3, samples=2),
        fatigue_consistency=_dim(72.0),
        strategy_execution=_dim(58.0),
        setup_sensitivity=_dim(50.0, confidence=0.4, samples=3),
        adaptation=_dim(64.0),
        overall_score=64.0,
        overall_confidence=0.62,
        percentile_vs_cohort=None,
        generated_by="scoring-engine@0.1.0",
    )


def test_driver_progress_snapshot_builds_with_ten_dimensions() -> None:
    snap = example_snapshot()
    assert snap.window == "rolling_30d"
    assert snap.braking.score == 74.0
    assert snap.adaptation.sample_count == 12
    assert snap.percentile_vs_cohort is None


def test_example_fixture_roundtrips_json() -> None:
    snap = example_snapshot()
    encoded = snap.model_dump_json()
    reloaded = DriverProgressSnapshot.model_validate_json(encoded)
    assert reloaded == snap


def test_endurance_dimensions_default_to_none_when_omitted() -> None:
    """T073 (sprint2-backend) — long_run_consistency, pace_decay,
    and tire_preservation are server-side endurance dims that
    sprint-only drivers will never have. They must default to
    None when omitted so the existing 10-dim fixture (and every
    snapshot already in the DB) keeps validating unchanged.
    Pin: additive non-breaking shape."""
    snap = example_snapshot()
    assert snap.long_run_consistency is None
    assert snap.pace_decay is None
    assert snap.tire_preservation is None


def test_endurance_dimensions_round_trip_when_set() -> None:
    """T073 — when the endurance pipeline (T070-T072 producers)
    fills these dims, they survive a JSON round-trip with the
    same SkillDimension shape as the per-lap dimensions.
    Mutation: dropping or coercing the fields would lose the
    endurance scoring on read for every endurance-active driver."""
    base = example_snapshot()
    enduro = SkillDimension(
        score=72.5, confidence=0.7, trend_14d="up",
        last_evidence_session_id=uuid6.uuid7(), sample_count=8,
    )
    snap = base.model_copy(
        update={
            "long_run_consistency": enduro,
            "pace_decay": enduro,
            "tire_preservation": enduro,
        }
    )
    encoded = snap.model_dump_json()
    reloaded = DriverProgressSnapshot.model_validate_json(encoded)
    assert reloaded.long_run_consistency == enduro
    assert reloaded.pace_decay == enduro
    assert reloaded.tire_preservation == enduro
    assert reloaded == snap


def test_driver_progress_snapshot_rejects_unknown_window() -> None:
    now = datetime(2026, 4, 24, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValidationError):
        DriverProgressSnapshot(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            captured_at=now,
            window="quarter",  # not in allowed literal set
            window_start=now - timedelta(days=90),
            window_end=now,
            braking=_dim(50.0),
            throttle_pickup=_dim(50.0),
            minimum_speed=_dim(50.0),
            line_consistency=_dim(50.0),
            tire_management=_dim(50.0),
            racecraft=_dim(50.0),
            fatigue_consistency=_dim(50.0),
            strategy_execution=_dim(50.0),
            setup_sensitivity=_dim(50.0),
            adaptation=_dim(50.0),
            overall_score=50.0,
            overall_confidence=0.5,
            percentile_vs_cohort=None,
            generated_by="v0",
        )
