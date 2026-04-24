from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.driver_benchmark_profile import (
    CohortDef,
    DriverBenchmarkProfile,
)
from lap_schemas.v1.environment import EnvironmentTag


def test_cohort_def_accepts_fully_scoped_cohort() -> None:
    cohort = CohortDef(
        skill_level="intermediate",
        car_class="gt3",
        track_id=uuid6.uuid7(),
        environment_tag=EnvironmentTag.SIM_PRACTICE,
        min_sessions=10,
    )
    assert cohort.skill_level == "intermediate"
    assert cohort.min_sessions == 10


def test_driver_benchmark_profile_accepts_with_archetype() -> None:
    profile = DriverBenchmarkProfile(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        generated_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
        cohort_definition=CohortDef(),
        cohort_size=42,
        per_track_car_percentiles={"spa/gt3-porsche": 0.72, "monza/gt3-ferrari": 0.58},
        per_dimension_percentiles={"braking": 0.65, "line_consistency": 0.80},
        archetype="smooth_flow",
    )
    assert profile.cohort_size == 42
    assert profile.archetype == "smooth_flow"
    assert profile.per_track_car_percentiles["spa/gt3-porsche"] == 0.72


def test_driver_benchmark_profile_rejects_unknown_archetype() -> None:
    with pytest.raises(ValidationError):
        DriverBenchmarkProfile(
            id=uuid6.uuid7(),
            driver_id=uuid6.uuid7(),
            generated_at=datetime(2026, 4, 24, tzinfo=timezone.utc),
            cohort_definition=CohortDef(),
            cohort_size=25,
            per_track_car_percentiles={},
            per_dimension_percentiles={},
            archetype="chaotic_neutral",  # not in allowed set
        )
