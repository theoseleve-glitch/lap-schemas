from pydantic import BaseModel, ConfigDict, Field


class PairingCreateResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pairing_token: str = Field(min_length=32)
