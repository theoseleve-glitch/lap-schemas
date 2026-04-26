"""lap_schemas.v1 — stable Pydantic data contracts for LAP.

Re-exports the core bundle-surface types consumers rely on. Adding
a new module to this package? Re-export it here so downstream users
can do ``from lap_schemas.v1 import SomeType`` instead of reaching
into individual modules.
"""

from lap_schemas.v1.action_outcome import (
    ActionOutcomeList,
    ActionOutcomeListItem,
)
from lap_schemas.v1.action_prescription import (
    ActionPrescriptionList,
    ActionPrescriptionListItem,
)
from lap_schemas.v1.billing import (
    BillingCheckoutRequest,
    BillingCheckoutResponse,
    BillingPlan,
    BillingPortalResponse,
)
from lap_schemas.v1.car_catalog import CarCatalogList, CarCatalogPublic
from lap_schemas.v1.coaching_rule import (
    CoachingRuleList,
    CoachingRulePublic,
)
from lap_schemas.v1.compare_case import (
    CompareCase,
    CompareCaseCreate,
    CompareCaseSessionSnapshot,
)
from lap_schemas.v1.device_session import DeviceSession
from lap_schemas.v1.driver_profile import DriverProfile, DriverProfileUpdate
from lap_schemas.v1.driver_profile_aggregate import DriverProfileAggregate
from lap_schemas.v1.lap_record import LapRecord
from lap_schemas.v1.next_actions import NextActionsResponse
from lap_schemas.v1.pairing import (
    PairingCreateResponse,
    PairingRedeemRequest,
    PairingRedeemResponse,
)
from lap_schemas.v1.session import SessionDetail, SessionManifest
from lap_schemas.v1.session_coaching_view import SessionCoachingView
from lap_schemas.v1.session_ingest import SessionIngestAccepted
from lap_schemas.v1.skill_drilldown import (
    SessionScoreRef,
    SkillDimensionName,
    SkillDrilldown,
    SkillTrendPoint,
)
from lap_schemas.v1.telemetry_sample import TelemetrySample
from lap_schemas.v1.timeline import TimelineEntry, TimelineResponse
from lap_schemas.v1.track_catalog import (
    SectorCheckpointPublic,
    TrackCatalogList,
    TrackCatalogPublic,
)
from lap_schemas.v1.user import User
from lap_schemas.v1.weakness_detail import (
    WeaknessDetail,
    WeaknessHistoryEntry,
)


__all__ = [
    "ActionOutcomeList",
    "ActionOutcomeListItem",
    "ActionPrescriptionList",
    "ActionPrescriptionListItem",
    "BillingCheckoutRequest",
    "BillingCheckoutResponse",
    "BillingPlan",
    "BillingPortalResponse",
    "CarCatalogList",
    "CarCatalogPublic",
    "CoachingRuleList",
    "CoachingRulePublic",
    "CompareCase",
    "CompareCaseCreate",
    "CompareCaseSessionSnapshot",
    "DeviceSession",
    "DriverProfile",
    "DriverProfileAggregate",
    "DriverProfileUpdate",
    "LapRecord",
    "NextActionsResponse",
    "PairingCreateResponse",
    "PairingRedeemRequest",
    "PairingRedeemResponse",
    "SectorCheckpointPublic",
    "SessionCoachingView",
    "SessionDetail",
    "SessionIngestAccepted",
    "SessionManifest",
    "SessionScoreRef",
    "SkillDimensionName",
    "SkillDrilldown",
    "SkillTrendPoint",
    "TelemetrySample",
    "TimelineEntry",
    "TimelineResponse",
    "TrackCatalogList",
    "TrackCatalogPublic",
    "User",
    "WeaknessDetail",
    "WeaknessHistoryEntry",
]
