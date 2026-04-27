"""T161-T165 — organization create / invitation shapes.

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

Invite role is `OrgInviteRole = Literal["coach", "driver"]` —
admin transfer is a separate concern (out of scope for T164).

Email regex is sanity-shape, not RFC-perfect (anything@anything.
anything) — avoids the `email-validator` dependency while still
rejecting obviously-malformed addresses.

Response omits no fields — `admin_user_id` is part of the public
shape because invitees / clients use it to decide whether to
show admin-only UI affordances. Invitation response includes
the `token` because email delivery isn't wired yet (T164 is the
infrastructure piece; email send is a later task).
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7

OrgPlan = Literal["free", "team", "pro"]
OrgInviteRole = Literal["coach", "driver"]
_EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


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


class OrganizationInvitationCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: str = Field(min_length=3, max_length=320, pattern=_EMAIL_REGEX)
    role: OrgInviteRole


class OrganizationInvitation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    org_id: UUID7
    email: str
    role: OrgInviteRole
    token: str
    created_at: datetime
    expires_at: datetime


class OrganizationMembership(BaseModel):
    """Returned by T165's accept-invite endpoint. Carries the
    new OrganizationMember row's identity + role so the client
    can route to the org and reflect the user's permissions.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    org_id: UUID7
    user_id: UUID7
    role: OrgInviteRole
    created_at: datetime


# Full role enum for list/listing-style shapes where admin
# entries appear alongside coach/driver. Distinct from
# OrgInviteRole, which excludes admin (admin transfer is not
# part of the invite/redeem flow).
OrgRole = Literal["admin", "coach", "driver"]


class OrganizationMemberEntry(BaseModel):
    """List-shape entry for T167's list-members endpoint.

    Same column set as OrganizationMembership but `role` admits
    the full {admin, coach, driver} space — listings include
    admins, accept-invite responses don't.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    org_id: UUID7
    user_id: UUID7
    role: OrgRole
    created_at: datetime


class OrganizationMemberList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: tuple[OrganizationMemberEntry, ...]
