import json

from lap_schemas.generate_openapi import build_openapi_document, main


def test_openapi_document_declares_version_3_1() -> None:
    doc = build_openapi_document()
    assert doc["openapi"].startswith("3.1")
    assert doc["info"]["title"]
    assert doc["info"]["version"]
    assert isinstance(doc["components"]["schemas"], dict)


def test_openapi_document_includes_every_v1_model() -> None:
    doc = build_openapi_document()
    schemas = doc["components"]["schemas"]
    expected = {
        "ActionOutcome",
        "ActionPrescription",
        "CoachingInsight",
        "CohortDef",
        "DataQuality",
        "DivergencePoint",
        "DriverBenchmarkProfile",
        "DriverProgressSnapshot",
        "DriverReadinessState",
        "LapRecord",
        "SensorConfig",
        "SensorConfigSnapshot",
        "SessionContext",
        "SessionManifest",
        "SessionRecord",
        "SkillDimension",
        "SuccessCondition",
        "TargetEvent",
        "TelemetrySample",
        "TransferLink",
        "WeaknessEpisode",
    }
    missing = expected - set(schemas.keys())
    assert not missing, f"missing schemas: {sorted(missing)}"


def test_main_writes_openapi_json_to_path(tmp_path) -> None:  # type: ignore[no-untyped-def]
    out = tmp_path / "openapi.json"
    exit_code = main([str(out)])
    assert exit_code == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["openapi"].startswith("3.1")
    assert "SessionManifest" in written["components"]["schemas"]
