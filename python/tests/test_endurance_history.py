"""T076 (sprint2-backend) — DriverEnduranceHistoryList response.

`GET /api/v1/driver/endurance/history` returns the events the
authenticated driver has been entered in (membership taken from
EnduranceEvent.driver_ids — explicit roster, not session-derived,
so pre-event entries appear before any logging happens).

Pinned by these tests:
  - the list accepts zero or more entries
  - each entry carries id, event_name, total_duration_seconds,
    stint_count (the planned-shape fields)
  - extra fields are forbidden (typo guard)
  - JSON round-trip preserves the entry list
"""

from __future__ import annotations

import uuid6
from pydantic import ValidationError

import pytest

from lap_schemas.v1.endurance_history import (
    DriverEnduranceHistoryEntry,
    DriverEnduranceHistoryList,
)


def test_history_list_accepts_empty_entries() -> None:
    """A driver who has never been entered in an endurance event
    sees an empty list, not 404. Pin: empty list is the sentinel
    for 'no history'."""
    response = DriverEnduranceHistoryList(events=())
    assert response.events == ()


def test_history_list_carries_planned_shape_per_entry() -> None:
    """Each entry exposes the planned-shape fields from the
    EnduranceEvent row. Pin id, event_name, total_duration_seconds,
    stint_count — clients use these for the history-card UI."""
    eid = uuid6.uuid7()
    entry = DriverEnduranceHistoryEntry(
        id=eid,
        event_name="Spa 24 Hours",
        total_duration_seconds=86400.0,
        stint_count=12,
    )
    response = DriverEnduranceHistoryList(events=(entry,))
    assert response.events[0].id == eid
    assert response.events[0].event_name == "Spa 24 Hours"
    assert response.events[0].total_duration_seconds == 86400.0
    assert response.events[0].stint_count == 12


def test_history_list_forbids_unknown_fields() -> None:
    """Producer-side typo (e.g. `event_id` instead of `id`) must
    raise — silent extras would let stale fields slip through and
    a future field rename would silently lose data."""
    with pytest.raises(ValidationError):
        DriverEnduranceHistoryList(
            events=(),
            unknown="boom",
        )


def test_history_entry_round_trips_json() -> None:
    """JSON round-trip for one entry preserves every field."""
    entry = DriverEnduranceHistoryEntry(
        id=uuid6.uuid7(),
        event_name="Petit Le Mans",
        total_duration_seconds=36000.0,
        stint_count=8,
    )
    response = DriverEnduranceHistoryList(events=(entry,))
    encoded = response.model_dump_json()
    reloaded = DriverEnduranceHistoryList.model_validate_json(encoded)
    assert reloaded == response
