"""T006 (sprint2-backend) — CompareCase.sessions snapshot field.

GET /api/v1/compare_cases/{id} now returns the case PLUS a
per-session snapshot block (`sessions`) computed from the
current SessionRecord rows. The snapshot is recomputed on every
GET, so when a referenced session reprocesses, the next GET
reflects the new values — no cache to invalidate because there
is no cache.

POST still returns CompareCase without the snapshot (the new
field is optional, default None) so T005's create-flow contract
is preserved.
"""

from datetime import datetime, timezone

import uuid6

from lap_schemas.v1.compare_case import (
    CompareCase,
    CompareCaseSessionSnapshot,
)


def _snapshot(**overrides: object) -> CompareCaseSessionSnapshot:
    base: dict[str, object] = {
        "session_id": uuid6.uuid7(),
        "processed_at": datetime(2026, 4, 26, tzinfo=timezone.utc),
        "best_lap_ms": 92_345,
        "total_laps": 12,
        "valid_laps": 11,
    }
    base.update(overrides)
    return CompareCaseSessionSnapshot(**base)  # type: ignore[arg-type]


def test_snapshot_round_trip() -> None:
    snap = _snapshot()
    revived = CompareCaseSessionSnapshot.model_validate_json(
        snap.model_dump_json()
    )
    assert revived == snap


def test_snapshot_allows_missing_record() -> None:
    """Some session_ids might not have a SessionRecord yet (still
    processing). The snapshot must encode that as nulls rather
    than crashing — clients render "still processing" for these."""
    minimal = CompareCaseSessionSnapshot(session_id=uuid6.uuid7())
    assert minimal.processed_at is None
    assert minimal.best_lap_ms is None
    assert minimal.total_laps is None
    assert minimal.valid_laps is None


def test_compare_case_supports_sessions_snapshot() -> None:
    """CompareCase gains an optional `sessions` field for T006."""
    case = CompareCase(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        session_ids=(uuid6.uuid7(), uuid6.uuid7()),
        rationale="x",
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
        sessions=(_snapshot(), _snapshot()),
    )
    assert case.sessions is not None
    assert len(case.sessions) == 2


def test_compare_case_sessions_default_is_none() -> None:
    """T005 contract: POST returns CompareCase WITHOUT sessions
    (the snapshot is a GET-time compute). Default = None preserves
    backwards-compat for the create-flow."""
    case = CompareCase(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        session_ids=(uuid6.uuid7(), uuid6.uuid7()),
        rationale="x",
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )
    assert case.sessions is None
