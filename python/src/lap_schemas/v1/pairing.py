from pydantic import BaseModel, ConfigDict, Field


class PairingCreateResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pairing_token: str = Field(min_length=32)


class PairingRedeemRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pairing_token: str = Field(min_length=32)


class PairingRedeemResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    refresh_token: str = Field(min_length=32)
