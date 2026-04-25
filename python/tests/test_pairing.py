import pytest
from pydantic import ValidationError

from lap_schemas.v1.pairing import PairingCreateResponse


def test_pairing_create_response_builds() -> None:
    r = PairingCreateResponse(pairing_token="x" * 32)
    assert r.pairing_token == "x" * 32


def test_pairing_create_response_rejects_short_token() -> None:
    with pytest.raises(ValidationError):
        PairingCreateResponse(pairing_token="too-short")


def test_pairing_create_response_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        PairingCreateResponse(
            pairing_token="x" * 32,
            unknown="oops",  # type: ignore[call-arg]
        )


def test_pairing_create_response_v1_reexport() -> None:
    from lap_schemas.v1 import PairingCreateResponse as Re

    assert Re is PairingCreateResponse
