package com.lap.schemas.v1

import kotlinx.serialization.Serializable

/**
 * Quantitative definition of "this prescription succeeded", mirroring
 * `lap_schemas.v1.success_condition`. Evaluated server-side when
 * subsequent sessions land (ADR-012).
 *
 * [comparison] literal is `"gte"` / `"lte"` / `"within_pct"`; when
 * `"within_pct"`, [targetPct] must be set. [measurementWindow] literal
 * is `"next_session"` / `"next_3_sessions"` / `"next_7_days"`. Both
 * kept as String until codegen.
 */
@Serializable
data class SuccessCondition(
    val metric: String,
    val targetValue: Double,
    val comparison: String,
    val measurementWindow: String,
    val targetPct: Double? = null,
)
