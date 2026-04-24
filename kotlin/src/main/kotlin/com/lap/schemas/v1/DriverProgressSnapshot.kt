package com.lap.schemas.v1

/**
 * Ten-axis driver skill rollup captured over a window, mirroring
 * `lap_schemas.v1.driver_progress_snapshot.DriverProgressSnapshot`.
 * One of the top-3 backend objects per ADR §5.1; mobile consumes +
 * renders on the driver dashboard.
 *
 * [window] literal is `"session"` / `"week"` / `"month"` /
 * `"rolling_30d"`; kept as String until codegen. Timestamps are RFC3339
 * UTC strings until T038. Pydantic bounds ([overallScore] in [0, 100],
 * [overallConfidence] + [percentileVsCohort] in [0, 1]) re-validated
 * server-side per ADR-012.
 */
data class DriverProgressSnapshot(
    val id: UUID7,
    val driverId: UUID7,
    val capturedAt: String,
    val window: String,
    val windowStart: String,
    val windowEnd: String,
    val braking: SkillDimension,
    val throttlePickup: SkillDimension,
    val minimumSpeed: SkillDimension,
    val lineConsistency: SkillDimension,
    val tireManagement: SkillDimension,
    val racecraft: SkillDimension,
    val fatigueConsistency: SkillDimension,
    val strategyExecution: SkillDimension,
    val setupSensitivity: SkillDimension,
    val adaptation: SkillDimension,
    val overallScore: Double,
    val overallConfidence: Double,
    val generatedBy: String,
    val percentileVsCohort: Double? = null,
)
