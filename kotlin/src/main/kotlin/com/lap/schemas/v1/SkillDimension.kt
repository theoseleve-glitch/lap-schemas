package com.lap.schemas.v1

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Per-skill rollup used inside [DriverProgressSnapshot], mirroring
 * `lap_schemas.v1.skill_dimension.SkillDimension`.
 *
 * [trend14d] is the `"up"` / `"flat"` / `"down"` / `"volatile"` literal;
 * kept as String until codegen. Pydantic constraints ([score] in
 * [0, 100], [confidence] in [0, 1], [sampleCount] >= 0) re-validated
 * server-side until T038.
 */
@Serializable
data class SkillDimension(
    val score: Double,
    val confidence: Double,
    @SerialName("trend_14d") val trend14d: String,
    val sampleCount: Int,
    val lastEvidenceSessionId: UUID7? = null,
)
