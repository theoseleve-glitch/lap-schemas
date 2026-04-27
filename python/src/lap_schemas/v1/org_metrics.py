"""T174 — org-level aggregate metrics shape.

Backs `GET /api/v1/orgs/:id/metrics` — admin or coach reads
roll-up KPIs for the org. Two metrics:

  - `wpd` (Weekly Paid Drivers, per-org variant): count of
    distinct drivers in the org with at least one session
    uploaded in the trailing 7 days. Mirrors the global
    `/admin/kpis` WPD definition but scoped to org members
    rather than paid users (org-level subscription is the
    paid status; individual drivers in an org don't need
    individual subscriptions).

  - `best_gain_dimension` + `best_gain_value`: across the
    org's drivers, the SkillDimensionName whose `score` has
    grown most (averaged across drivers) over the trailing
    30 days. `None` when there's not enough data — e.g.,
    drivers with only one snapshot can't have a delta;
    drivers with no snapshots at all also contribute nothing.

The endpoint is the at-a-glance pulse for an org admin: how
active is my team this week, and where's the team gaining the
most ground? Distinct from T171's per-driver dashboard which
lists individual drivers.

Both metrics tolerate the empty-org case: wpd=0 and gain
fields = None for an org with no drivers, no sessions, or
fewer than 2 snapshots per driver. The endpoint never 5xx's
on data thinness.
"""

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.skill_drilldown import SkillDimensionName


class OrgMetrics(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    wpd: int = Field(ge=0)
    best_gain_dimension: SkillDimensionName | None = None
    best_gain_value: float | None = None
