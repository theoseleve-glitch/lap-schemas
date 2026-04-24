package com.lap.schemas.v1

/**
 * Per-skill rollup used inside [DriverProgressSnapshot], mirroring
 * `lap_schemas.v1.skill_dimension.SkillDimension`.
 *
 * [trend14d] is the `"up"` / `"flat"` / `"down"` / `"volatile"` literal;
 * kept as String until codegen. Pydantic constraints ([score] in
 * [0, 100], [confidence] in [0, 1], [sampleCount] >= 0) re-validated
 * server-side until T038.
 */
data class SkillDimension(
    val score: Double,
    val confidence: Double,
    val trend14d: String,
    val sampleCount: Int,
    val lastEvidenceSessionId: UUID7? = null,
)
