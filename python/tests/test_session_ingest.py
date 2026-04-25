import pytest
from pydantic import ValidationError

from lap_schemas.v1.session_ingest import SessionIngestAccepted


def test_session_ingest_accepted_builds() -> None:
    r = SessionIngestAccepted(status="accepted")
    assert r.status == "accepted"


def test_session_ingest_accepted_rejects_other_status() -> None:
    with pytest.raises(ValidationError):
        SessionIngestAccepted(status="processing")  # type: ignore[arg-type]


def test_session_ingest_accepted_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        SessionIngestAccepted(
            status="accepted",
            extra="oops",  # type: ignore[call-arg]
        )


def test_session_ingest_accepted_v1_reexport() -> None:
    from lap_schemas.v1 import SessionIngestAccepted as Re

    assert Re is SessionIngestAccepted
