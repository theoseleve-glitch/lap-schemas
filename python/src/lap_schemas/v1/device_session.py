from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7


class DeviceSession(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    created_at: datetime
