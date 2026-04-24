package com.lap.schemas.v1

/**
 * One sensor's runtime config: which sensor it is, how fast it's sampled,
 * whether it's turned on for this session. Pydantic enforces
 * `sampleRateHz > 0`; re-validated server-side per ADR-012 until T038
 * wires kotlinx-serialization contracts.
 */
data class SensorConfig(
    val name: String,
    val sampleRateHz: Double,
    val enabled: Boolean = true,
)

/**
 * Snapshot of the capture device's sensor stack at session start,
 * mirroring `lap_schemas.v1.sensor_config.SensorConfigSnapshot`. Ships
 * with every bundle manifest so ingestion can validate per-sample
 * provenance (T139 populates this from the live capture config).
 */
data class SensorConfigSnapshot(
    val sensors: List<SensorConfig> = emptyList(),
    val hardwareId: String? = null,
    val firmwareVersion: String? = null,
)
