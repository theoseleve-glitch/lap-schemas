from typing import Literal

from pydantic import BaseModel, ConfigDict


class SessionIngestAccepted(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: Literal["accepted"]
