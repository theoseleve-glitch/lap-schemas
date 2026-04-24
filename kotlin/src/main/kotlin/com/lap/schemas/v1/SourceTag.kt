package com.lap.schemas.v1

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Session-level data source, promoted to a typed enum from the stub
 * String that T027 carried on [SessionManifest.source]. Wire values
 * match the Python `lap_schemas.v1.source.SourceTag` Literal byte-for-byte
 * — ingestion (ADR-012) rejects manifests that use anything else.
 */
@Serializable
enum class SourceTag(val wireValue: String) {
    @SerialName("iracing") IRACING("iracing"),
    @SerialName("acc") ACC("acc"),
    @SerialName("ac") AC("ac"),
    @SerialName("ams2") AMS2("ams2"),
    @SerialName("rf2") RF2("rf2"),
    @SerialName("lmu") LMU("lmu"),
    @SerialName("rennsport") RENNSPORT("rennsport"),
    @SerialName("f1_game") F1_GAME("f1_game"),
    @SerialName("real") REAL("real"),
    ;

    companion object {
        fun fromWire(value: String): SourceTag =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown SourceTag wire value: '$value'")
    }
}
