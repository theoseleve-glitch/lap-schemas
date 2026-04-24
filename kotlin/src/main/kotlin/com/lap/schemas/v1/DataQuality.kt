package com.lap.schemas.v1

/**
 * Per-session data-quality verdict, mirroring
 * `lap_schemas.v1.data_quality.DataQuality`. Populated by the capture
 * client at finalize time; surfaces to the user via the Uploads screen
 * and gates which downstream consumers may use the session.
 *
 * Pydantic enforces `score` and `channelCompleteness` in [0, 100] and
 * non-negative counters. These constraints aren't enforced at the Kotlin
 * layer yet — ingest re-validates server-side (ADR-012). Kotlin
 * enforcement lands when kotlinx-serialization contracts arrive in T038.
 *
 * [warnings] and [recommendations] default to empty lists to match the
 * Pydantic `default_factory=tuple`.
 */
data class DataQuality(
    val score: Double,
    val channelCompleteness: Double,
    val sampleGapsCount: Int,
    val sampleRateStability: Double,
    val usableForOverlays: Boolean,
    val usableForLongTermCoaching: Boolean,
    val gpsFixQuality: Double? = null,
    val gpsSatelliteCountAvg: Int? = null,
    val warnings: List<String> = emptyList(),
    val recommendations: List<String> = emptyList(),
)
