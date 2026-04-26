"""T005 (sprint2-backend) — CompareCase schemas (CRUD payloads).

A CompareCase is a saved A/B (or N-way) comparison the user
asked the system to remember — like "why was I slower at Spa
last week?" preserved as a durable artifact instead of a
one-shot query.

`CompareCaseCreate` is the POST input (session IDs + rationale).
`CompareCase` is the persisted/returned shape (adds id, driver_id,
created_at).

T006 will add an auto-updating outcome block when referenced
sessions reprocess — out of scope for T005's CRUD-only contract.
"""

from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.compare_case import CompareCase, CompareCaseCreate


# -- create ------------------------------------------------------


def test_create_round_trips_with_two_session_ids() -> None:
    payload = CompareCaseCreate(
        session_ids=(uuid6.uuid7(), uuid6.uuid7()),
        rationale="Why was Spa slower last week?",
    )
    revived = CompareCaseCreate.model_validate_json(payload.model_dump_json())
    assert revived == payload


def test_create_rejects_single_session() -> None:
    """A 'comparison' of one session is meaningless — pin the
    minimum at 2 so callers can't create degenerate cases."""
    with pytest.raises(ValidationError):
        CompareCaseCreate(
            session_ids=(uuid6.uuid7(),),
            rationale="...",
        )


def test_create_rejects_empty_rationale() -> None:
    """Rationale captures the *why* — without it, the case is
    just a session-ID list with no context for revisiting later."""
    with pytest.raises(ValidationError):
        CompareCaseCreate(
            session_ids=(uuid6.uuid7(), uuid6.uuid7()),
            rationale="",
        )


def test_create_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        CompareCaseCreate(  # type: ignore[call-arg]
            session_ids=(uuid6.uuid7(), uuid6.uuid7()),
            rationale="ok",
            unknown="oops",
        )


# -- persisted shape --------------------------------------------


def test_compare_case_round_trips() -> None:
    case = CompareCase(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        session_ids=(uuid6.uuid7(), uuid6.uuid7()),
        rationale="practice setup A vs B",
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )
    revived = CompareCase.model_validate_json(case.model_dump_json())
    assert revived == case


def test_compare_case_supports_more_than_two_sessions() -> None:
    """N-way compares (3+ sessions) are allowed — the cap is
    on the lower bound, not the upper bound."""
    case = CompareCase(
        id=uuid6.uuid7(),
        driver_id=uuid6.uuid7(),
        session_ids=tuple(uuid6.uuid7() for _ in range(5)),
        rationale="setup sweep",
        created_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )
    assert len(case.session_ids) == 5
