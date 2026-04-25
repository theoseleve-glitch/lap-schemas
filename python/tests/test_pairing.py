import pytest
from pydantic import ValidationError

from lap_schemas.v1.pairing import (
    PairingCreateResponse,
    PairingRedeemRequest,
    PairingRedeemResponse,
)


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


def test_pairing_redeem_request_builds() -> None:
    r = PairingRedeemRequest(pairing_token="y" * 32)
    assert r.pairing_token == "y" * 32


def test_pairing_redeem_request_rejects_short_token() -> None:
    with pytest.raises(ValidationError):
        PairingRedeemRequest(pairing_token="too-short")


def test_pairing_redeem_request_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        PairingRedeemRequest(
            pairing_token="y" * 32,
            extra="oops",  # type: ignore[call-arg]
        )


def test_pairing_redeem_response_builds() -> None:
    r = PairingRedeemResponse(refresh_token="z" * 32)
    assert r.refresh_token == "z" * 32


def test_pairing_redeem_response_rejects_short_refresh_token() -> None:
    with pytest.raises(ValidationError):
        PairingRedeemResponse(refresh_token="short")


def test_pairing_redeem_v1_reexport() -> None:
    from lap_schemas.v1 import PairingRedeemRequest as ReReq
    from lap_schemas.v1 import PairingRedeemResponse as ReResp

    assert ReReq is PairingRedeemRequest
    assert ReResp is PairingRedeemResponse
