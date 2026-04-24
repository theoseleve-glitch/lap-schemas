package com.lap.schemas.v1

/**
 * Consumer-side mirror of `lap_schemas.v1.weakness_episode.WeaknessEpisode`.
 *
 * The backend owns weakness detection (ADR-012: no local coaching logic
 * on mobile beyond rule-engine execution); the mobile app caches these
 * episodes in InsightCacheEntity (T045) for offline dashboard view.
 *
 * Literals [severity] (`low`/`medium`/`high`) and [status]
 * (`open`/`improving`/`resolved`/`dormant`) are kept as String until
 * codegen. Timestamps are RFC3339 UTC strings; T038 moves them onto
 * kotlinx-datetime Instants.
 *
 * Pydantic constraints: [recurrenceCount] >= 0, [confidence] in [0, 1],
 * [confidenceDecayPerDay] >= 0, [sessionsAffected] max length 50.
 * Re-validated server-side per ADR-012 until T038.
 */
data class WeaknessEpisode(
    val id: UUID7,
    val driverId: UUID7,
    val category: WeaknessCategory,
    val subcategory: String,
    val firstObservedAt: String,
    val lastObservedAt: String,
    val recurrenceCount: Int,
    val severity: String,
    val confidence: Double,
    val status: String,
    val libraryRuleId: String,
    val cornerTag: String? = null,
    val environmentScope: List<EnvironmentTag> = emptyList(),
    val sessionsAffected: List<UUID7> = emptyList(),
    val confidenceDecayPerDay: Double = 0.02,
    val resolvedAt: String? = null,
    val linkedPrescriptions: List<UUID7> = emptyList(),
    val linkedInsights: List<UUID7> = emptyList(),
)
