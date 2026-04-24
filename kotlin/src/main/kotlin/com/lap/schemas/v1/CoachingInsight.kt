package com.lap.schemas.v1

/**
 * Per-session coaching finding that the mobile dashboard renders inline
 * and the InsightCache (T045) caches for offline view. Backend-authored
 * per ADR-012 (no local coaching logic on mobile beyond rule-engine
 * execution).
 *
 * **No Pydantic source for CoachingInsight exists yet** — this stub
 * captures the mobile-facing rendering subset derived from the 6-month
 * roadmap doc (`docs/additional help for more roadmap context/
 * lap_roadmap_6months.md:267`). The following nested types the spec
 * mentions are deferred until the canonical Pydantic lands:
 *  - `Evidence` (telemetry span refs + chart preset)
 *  - `MeasurableTarget`
 *
 * [severity] literal is `"INFO"` / `"LOW"` / `"MED"` / `"HIGH"`;
 * [displayLevel] is `"BEGINNER"` / `"INTERMEDIATE"` / `"ADVANCED"`.
 * Both kept as String until codegen; timestamps are RFC3339 UTC
 * strings until T038.
 */
data class CoachingInsight(
    val id: UUID7,
    val sessionId: UUID7,
    val driverId: UUID7,
    val observation: String,
    val likelyCause: String,
    val action: String,
    val confidence: Double,
    val severity: String,
    val displayLevel: String,
    val reviewLaterAt: String? = null,
    val createdAt: String? = null,
)
