"""Billing wire schemas (T148).

Stripe Checkout session creation request + response. The plan
literal is the canonical name; backend translates it to a Stripe
price_id at request time.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

BillingPlan = Literal["lap_monthly", "lap_yearly", "waitlist_founder"]


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
