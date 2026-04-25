"""lap_schemas.v1 — stable Pydantic data contracts for LAP.

Re-exports the core bundle-surface types consumers rely on. Adding
a new module to this package? Re-export it here so downstream users
can do ``from lap_schemas.v1 import SomeType`` instead of reaching
into individual modules.
"""

from lap_schemas.v1.car_catalog import CarCatalogList, CarCatalogPublic
from lap_schemas.v1.device_session import DeviceSession
from lap_schemas.v1.driver_profile import DriverProfile, DriverProfileUpdate
from lap_schemas.v1.lap_record import LapRecord
from lap_schemas.v1.pairing import (
    PairingCreateResponse,
    PairingRedeemRequest,
    PairingRedeemResponse,
)
from lap_schemas.v1.session import SessionDetail, SessionManifest
from lap_schemas.v1.session_ingest import SessionIngestAccepted
from lap_schemas.v1.telemetry_sample import TelemetrySample
from lap_schemas.v1.track_catalog import (
    SectorCheckpointPublic,
    TrackCatalogList,
    TrackCatalogPublic,
)
from lap_schemas.v1.user import User


__all__ = [
    "CarCatalogList",
    "CarCatalogPublic",
    "DeviceSession",
    "DriverProfile",
    "DriverProfileUpdate",
    "LapRecord",
    "PairingCreateResponse",
    "PairingRedeemRequest",
    "PairingRedeemResponse",
    "SectorCheckpointPublic",
    "SessionDetail",
    "SessionIngestAccepted",
    "SessionManifest",
    "TelemetrySample",
    "TrackCatalogList",
    "TrackCatalogPublic",
    "User",
]
