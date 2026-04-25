from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from lap_schemas.v1.ids import UUID7

SubscriptionStatus = Literal["inactive", "trial", "active", "past_due", "cancelled"]


class User(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    clerk_user_id: str
    email: str
    created_at: datetime
    subscription_status: SubscriptionStatus
    is_admin: bool
