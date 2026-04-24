package com.lap.schemas.v1

/**
 * Hand-typed stub mirroring `lap_schemas.v1.session.SessionManifest`
 * (Pydantic v2). Codegen isn't wired yet; this keeps mobile unblocked.
 *
 * Scope of T027:
 *  - Only SessionManifest is the deliverable; [DataQuality] and
 *    [SensorConfigSnapshot] are empty placeholders populated by T031/T032.
 *  - Enum-like fields ([environmentTag], [captureApp], etc.) stay as
 *    String until T030 (EnvironmentTag) promotes them to enums; [source]
 *    was promoted in T029. [UUID7] hardens in T039.
 *  - Serialization annotations land in T038. Do not add @Serializable here.
 */

/** Placeholder UUIDv7 alias until T039 introduces validation. */
typealias UUID7 = String

/** Placeholder populated by T031. */
data class DataQuality(val placeholder: Unit = Unit)

/** Placeholder populated by T032. */
data class SensorConfigSnapshot(val placeholder: Unit = Unit)

data class SessionManifest(
    val sessionId: UUID7,
    val driverId: UUID7,
    val bundleVersion: String,
    val captureApp: String,
    val captureAppVersion: String,
    val deviceModel: String,
    val deviceOs: String,
    val deviceOsVersion: String,
    val source: SourceTag,
    val simTitle: String? = null,
    val realHardware: String? = null,
    val carId: UUID7,
    val trackId: UUID7,
    val trackLayout: String,
    val environmentTag: String,
    val objectiveTag: String? = null,
    val trainingBlockId: UUID7? = null,
    val startedAt: String,
    val endedAt: String,
    val durationSeconds: Double,
    val telemetryChecksums: Map<String, String>,
    val totalSamples: Int,
    val sampleRateHz: Double,
    val dataQuality: DataQuality,
    val sensorConfig: SensorConfigSnapshot,
)
