from typing import Literal

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7


class SessionIngestAccepted(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: Literal["accepted"]
    session_id: UUID7
    ingest_job_id: str
    status_stream_url: str
