package com.lap.schemas.v1

/**
 * One completed lap, mirroring `lap_schemas.v1.lap_record.LapRecord`.
 *
 * Lap and sector detection happens server-side from raw GPS (ADR-012);
 * this record is written by ingestion and consumed by the mobile app
 * for dashboard overlays and cached offline in InsightCacheEntity (T045).
 *
 * Pydantic constraints: [lapNumber] >= 0, [timeMs] >= 0 when present.
 * Re-validated server-side until T038 wires kotlinx-serialization.
 */
data class LapRecord(
    val id: UUID7,
    val sessionId: UUID7,
    val lapNumber: Int,
    val timeMs: Int? = null,
    val sectorTimesMs: List<Int> = emptyList(),
    val valid: Boolean = true,
    val flags: List<String> = emptyList(),
)
