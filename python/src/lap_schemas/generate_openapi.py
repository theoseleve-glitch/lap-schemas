from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from lap_schemas.v1.action_outcome import ActionOutcome
from lap_schemas.v1.action_prescription import ActionPrescription
from lap_schemas.v1.coaching_insight import CoachingInsight
from lap_schemas.v1.data_quality import DataQuality
from lap_schemas.v1.divergence_point import DivergencePoint
from lap_schemas.v1.driver_benchmark_profile import CohortDef, DriverBenchmarkProfile
from lap_schemas.v1.driver_progress_snapshot import DriverProgressSnapshot
from lap_schemas.v1.driver_readiness_state import DriverReadinessState, TargetEvent
from lap_schemas.v1.lap_record import LapRecord
from lap_schemas.v1.sensor_config import SensorConfig, SensorConfigSnapshot
from lap_schemas.v1.session import SessionManifest
from lap_schemas.v1.session_context import SessionContext
from lap_schemas.v1.session_record import SessionRecord
from lap_schemas.v1.skill_dimension import SkillDimension
from lap_schemas.v1.success_condition import SuccessCondition
from lap_schemas.v1.telemetry_sample import TelemetrySample
from lap_schemas.v1.transfer_link import TransferLink
from lap_schemas.v1.weakness_episode import WeaknessEpisode

MODELS: tuple[type[BaseModel], ...] = (
    ActionOutcome,
    ActionPrescription,
    CoachingInsight,
    CohortDef,
    DataQuality,
    DivergencePoint,
    DriverBenchmarkProfile,
    DriverProgressSnapshot,
    DriverReadinessState,
    LapRecord,
    SensorConfig,
    SensorConfigSnapshot,
    SessionContext,
    SessionManifest,
    SessionRecord,
    SkillDimension,
    SuccessCondition,
    TargetEvent,
    TelemetrySample,
    TransferLink,
    WeaknessEpisode,
)

_REF_TEMPLATE = "#/components/schemas/{model}"


def build_openapi_document() -> dict[str, Any]:
    schemas: dict[str, Any] = {}
    for model in MODELS:
        schema = model.model_json_schema(ref_template=_REF_TEMPLATE)
        nested = schema.pop("$defs", {})
        schemas[model.__name__] = schema
        for name, sub in nested.items():
            schemas.setdefault(name, sub)
    return {
        "openapi": "3.1.0",
        "info": {"title": "lap-schemas", "version": "v1"},
        "paths": {},
        "components": {"schemas": schemas},
    }


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    out = Path(args[0]) if args else Path("openapi.json")
    doc = build_openapi_document()
    out.write_text(json.dumps(doc, indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
