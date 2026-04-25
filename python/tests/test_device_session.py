from datetime import datetime, timezone

import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.device_session import DeviceSession


def test_device_session_builds() -> None:
    d = DeviceSession(
        id=uuid6.uuid7(),
        created_at=datetime(2026, 4, 25, 10, 0, tzinfo=timezone.utc),
    )
    assert d.created_at.tzinfo is timezone.utc


def test_device_session_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        DeviceSession(
            id=uuid6.uuid7(),
            created_at=datetime(2026, 4, 25, 10, 0, tzinfo=timezone.utc),
            unknown="oops",  # type: ignore[call-arg]
        )


def test_device_session_v1_reexport() -> None:
    from lap_schemas.v1 import DeviceSession as Re

    assert Re is DeviceSession
