"""Billing wire schemas (T148, T177).

Stripe Checkout session creation request + response. The plan
literal is the canonical name; backend translates it to a Stripe
price_id at request time.

T177 adds three B2B pricing tiers:
  - b2b_5seat:    5 driver seats, fixed monthly
  - b2b_15seat:   15 driver seats, fixed monthly
  - b2b_unlimited: no seat cap (priced per-driver-active or
    flat-rate, set in the Stripe dashboard)

Tier selection drives both the Stripe price_id and the org's
seats_limit at provisioning; the seat-cap enforcement (T170 402
on invite) reads `seats_limit` independently, so the price
literal here doesn't carry the cap value — it's only the
plan_id ↔ price_id binding.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

BillingPlan = Literal[
    "lap_monthly",
    "lap_yearly",
    "waitlist_founder",
    "b2b_5seat",
    "b2b_15seat",
    "b2b_unlimited",
]


class BillingCheckoutRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    plan: BillingPlan


class BillingCheckoutResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    url: str
    session_id: str


class BillingPortalResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    url: str
