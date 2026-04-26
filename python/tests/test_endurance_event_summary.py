"""T075 (sprint2-backend) — EnduranceEventSummary response model.

Pinned by these tests:
  - the model accepts a fully-populated event (planned shape +
    recorded aggregates)
  - mean_lap_time_decay_seconds and mean_fuel_used_liters default
    to None when no stints have been recorded — clients must
    distinguish "no data" from a real 0.0 (perfect preservation)
  - extra fields are forbidden (typo guard)
  - JSON round-trip preserves every field including the nullable
    aggregates
"""

from __future__ import annotations

import uuid6
from pydantic import ValidationError

import pytest

from lap_schemas.v1.endurance_event_summary import EnduranceEventSummary


def test_summary_accepts_full_payload_with_recorded_aggregates() -> None:
    drivers = [str(uuid6.uuid7()) for _ in range(3)]
    summary = EnduranceEventSummary(
        id=uuid6.uuid7(),
        event_name="Spa 24 Hours 2026",
        total_duration_seconds=86400.0,
        stint_count=12,
        driver_ids=drivers,
        recorded_session_count=4,
        recorded_stint_count=8,
        mean_lap_time_decay_seconds=0.07,
        mean_fuel_used_liters=39.5,
    )
    assert summary.event_name == "Spa 24 Hours 2026"
    assert summary.recorded_stint_count == 8
    assert summary.mean_lap_time_decay_seconds == 0.07
    assert summary.mean_fuel_used_liters == 39.5


def test_aggregates_default_to_none_when_no_stints_recorded() -> None:
    """Empty endurance weekend (event scheduled, no sessions yet)
    → recorded_stint_count == 0 and the means default to None.
    Pin: clients distinguish "no stints recorded" from "perfect
    0.0 preservation"; coercing to 0.0 would mis-render UI."""
    summary = EnduranceEventSummary(
        id=uuid6.uuid7(),
        event_name="Future Event",
        total_duration_seconds=43200.0,
        stint_count=10,
        driver_ids=[str(uuid6.uuid7())],
        recorded_session_count=0,
        recorded_stint_count=0,
    )
    assert summary.mean_lap_time_decay_seconds is None
    assert summary.mean_fuel_used_liters is None


def test_summary_forbids_unknown_fields() -> None:
    """A typoed field name on the producer side (e.g.
    `mean_pace_decay` instead of `mean_lap_time_decay_seconds`)
    must raise — silent extras would let the client see stale
    or missing data."""
    with pytest.raises(ValidationError):
        EnduranceEventSummary(
            id=uuid6.uuid7(),
            event_name="Bad",
            total_duration_seconds=3600.0,
            stint_count=2,
            driver_ids=[],
            recorded_session_count=0,
            recorded_stint_count=0,
            unknown_field="boom",
        )


def test_summary_round_trips_json_with_null_aggregates() -> None:
    """JSON round-trip with mean_*_seconds = None preserves the
    null on both ends. Mutation: a Pydantic field that lost the
    `| None` would fail this round-trip on the empty-event case."""
    original = EnduranceEventSummary(
        id=uuid6.uuid7(),
        event_name="Empty",
        total_duration_seconds=3600.0,
        stint_count=2,
        driver_ids=[str(uuid6.uuid7())],
        recorded_session_count=0,
        recorded_stint_count=0,
    )
    encoded = original.model_dump_json()
    reloaded = EnduranceEventSummary.model_validate_json(encoded)
    assert reloaded == original
    assert reloaded.mean_lap_time_decay_seconds is None
