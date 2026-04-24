package com.lap.schemas.v1

/**
 * Backend-generated prescription for a specific driver weakness,
 * mirroring `lap_schemas.v1.action_prescription.ActionPrescription`.
 * Mobile consumes + displays; no local prescription authoring
 * (ADR-012). Cached in PrescriptionCacheEntity (T046) for offline
 * view.
 *
 * [priority] literal is `"p0"` / `"p1"` / `"p2"`; [status] literal is
 * `"proposed"` / `"accepted"` / `"in_progress"` / `"completed"` /
 * `"skipped"` / `"expired"`. Both kept as String until codegen.
 * Timestamps are RFC3339 UTC strings until T038.
 */
data class ActionPrescription(
    val id: UUID7,
    val driverId: UUID7,
    val createdAt: String,
    val priority: String,
    val title: String,
    val rationale: String,
    val expectedContext: SessionContext,
    val successCondition: SuccessCondition,
    val status: String,
    val weaknessEpisodeId: UUID7? = null,
    val dueBeforeSessionId: UUID7? = null,
    val validUntil: String? = null,
    val drillTemplateId: String? = null,
    val acceptedAt: String? = null,
    val outcomeId: UUID7? = null,
)
