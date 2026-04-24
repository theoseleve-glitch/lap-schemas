package com.lap.schemas.v1

/**
 * Hand-typed stub mirroring `lap_schemas.v1.session.SessionManifest`
 * (Pydantic v2). Codegen isn't wired yet; this keeps mobile unblocked.
 *
 * Scope of remaining refinements:
 *  - Remaining enum-like fields ([captureApp], [realHardware],
 *    [objectiveTag], [bundleVersion]) stay as String until codegen
 *    lands. [source] promoted in T029, [environmentTag] in T030,
 *    [dataQuality] filled in T031, [sensorConfig] in T032.
 *    [UUID7] hardens in T039.
 *  - Serialization annotations land in T038. Do not add @Serializable here.
 */

/** Placeholder UUIDv7 alias until T039 introduces validation. */
typealias UUID7 = String

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
    val environmentTag: EnvironmentTag,
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
