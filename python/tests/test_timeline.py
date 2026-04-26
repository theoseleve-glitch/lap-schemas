"""T001 (sprint2-backend) — TimelineEntry + TimelineResponse schemas.

The driver timeline is the list view at /api/v1/driver/timeline.
TimelineEntry is the per-row summary (lighter than the full
SessionRecord at /api/v1/sessions/:id), TimelineResponse wraps
a page of entries with an opaque next_cursor.

The schemas here are deliberately additive and frozen — they
go on the wire so tests pin the shape to prevent silent drift.
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.timeline import TimelineEntry, TimelineResponse


def _entry(**overrides: object) -> TimelineEntry:
    base: dict[str, object] = {
        "session_id": uuid6.uuid7(),
        "processed_at": datetime(2026, 4, 26, 12, 0, tzinfo=timezone.utc),
        "best_lap_ms": 92_345,
        "total_laps": 12,
        "valid_laps": 11,
        "badges": ["personal_best"],
    }
    base.update(overrides)
    return TimelineEntry(**base)  # type: ignore[arg-type]


def test_timeline_entry_round_trip() -> None:
    entry = _entry()
    json_str = entry.model_dump_json()
    revived = TimelineEntry.model_validate_json(json_str)
    assert revived == entry


def test_timeline_entry_defaults_empty_badges() -> None:
    entry = _entry()
    minimal = TimelineEntry(
        session_id=entry.session_id,
        processed_at=entry.processed_at,
    )
    assert minimal.badges == []
    assert minimal.total_laps == 0
    assert minimal.valid_laps == 0
    assert minimal.best_lap_ms is None


def test_timeline_entry_rejects_negative_lap_count() -> None:
    with pytest.raises(ValidationError):
        _entry(total_laps=-1)


def test_timeline_entry_rejects_negative_best_lap_ms() -> None:
    with pytest.raises(ValidationError):
        _entry(best_lap_ms=-5)


def test_timeline_entry_rejects_extra_fields() -> None:
    """Frozen + extra=forbid prevents accidental wire-format
    drift via stray fields."""
    with pytest.raises(ValidationError):
        TimelineEntry(  # type: ignore[call-arg]
            session_id=uuid6.uuid7(),
            processed_at=datetime.now(timezone.utc),
            unknown_field="oops",
        )


def test_timeline_response_with_entries_and_cursor() -> None:
    entries = [_entry(), _entry(badges=[])]
    resp = TimelineResponse(entries=entries, next_cursor="opaque-cursor-token")
    json_str = resp.model_dump_json()
    revived = TimelineResponse.model_validate_json(json_str)
    assert revived.entries == tuple(entries) or revived.entries == entries
    assert revived.next_cursor == "opaque-cursor-token"


def test_timeline_response_empty_page_has_null_cursor() -> None:
    """An empty timeline must serialize cleanly — next_cursor None
    means "no more pages" and is the natural terminal."""
    resp = TimelineResponse(entries=[], next_cursor=None)
    parsed = TimelineResponse.model_validate_json(resp.model_dump_json())
    assert list(parsed.entries) == []
    assert parsed.next_cursor is None


def test_timeline_response_default_cursor_is_none() -> None:
    resp = TimelineResponse(entries=[])
    assert resp.next_cursor is None
