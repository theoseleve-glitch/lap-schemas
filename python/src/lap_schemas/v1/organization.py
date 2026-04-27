"""T161-T165 — organization create / response shapes.

Backs `POST /api/v1/orgs` (T163), `POST /api/v1/orgs/:id/invites`
(T164), and `POST /api/v1/orgs/:id/invites/:token/accept` (T165).

The Organization is a multi-user shared workspace with its own
billing tier (`plan`), seat cap (`seats_limit`), and admin
(`admin_user_id`). Distinct from User / DriverProfile which are
individual-scoped.

Bounds:
  - `name` ∈ [1, 120] chars: empty would be unnamable in the UI
    list (reject at the boundary so the persisted set is always
    discriminable); 120 matches the ORM column width.
  - `plan` is a closed-set Literal: free / team / pro. The DB
    stores it as String(32) without CHECK; the boundary is the
    schema layer, consistent with similar enums (skill_level,
    subscription_status).
  - `seats_limit` >= 1: zero would mean nobody can be a member,
    which is nonsensical; the cap must allow at least the admin.

Response omits no fields — `admin_user_id` is part of the public
shape because invitees / clients use it to decide whether to
show admin-only UI affordances.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

OrgPlan = Literal["free", "team", "pro"]


class OrganizationCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    plan: OrgPlan = "free"
    seats_limit: int = Field(ge=1)


class Organization(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    name: str
    plan: OrgPlan
    admin_user_id: UUID7
    seats_limit: int
    created_at: datetime
