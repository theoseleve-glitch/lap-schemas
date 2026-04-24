package com.lap.schemas.v1

/**
 * Session-level data source, promoted to a typed enum from the stub
 * String that T027 carried on [SessionManifest.source]. Wire values
 * match the Python `lap_schemas.v1.source.SourceTag` Literal byte-for-byte
 * — ingestion (ADR-012) rejects manifests that use anything else.
 *
 * @SerialName wiring arrives in T038 when schema types become
 * kotlinx-serialization round-trippable.
 */
enum class SourceTag(val wireValue: String) {
    IRACING("iracing"),
    ACC("acc"),
    AC("ac"),
    AMS2("ams2"),
    RF2("rf2"),
    LMU("lmu"),
    RENNSPORT("rennsport"),
    F1_GAME("f1_game"),
    REAL("real"),
    ;

    companion object {
        fun fromWire(value: String): SourceTag =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown SourceTag wire value: '$value'")
    }
}
