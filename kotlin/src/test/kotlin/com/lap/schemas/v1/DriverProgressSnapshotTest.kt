package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/**
 * Locks the DriverProgressSnapshot + SkillDimension shapes. Backend-
 * generated and consumer-rendered on mobile (ADR-012).
 */
class DriverProgressSnapshotTest {
    private fun dim(score: Double, trend: String = "flat") = SkillDimension(
        score = score,
        confidence = 0.8,
        trend14d = trend,
        sampleCount = 42,
    )

    @Test
    fun can_build_rolling_snapshot_with_all_ten_dimensions() {
        val snap = DriverProgressSnapshot(
            id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa1",
            driverId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            capturedAt = "2026-04-24T10:00:00Z",
            window = "rolling_30d",
            windowStart = "2026-03-25T00:00:00Z",
            windowEnd = "2026-04-24T00:00:00Z",
            braking = dim(78.0, "up"),
            throttlePickup = dim(65.0),
            minimumSpeed = dim(72.0),
            lineConsistency = dim(81.0, "up"),
            tireManagement = dim(55.0, "down"),
            racecraft = dim(70.0),
            fatigueConsistency = dim(60.0, "volatile"),
            strategyExecution = dim(58.0),
            setupSensitivity = dim(50.0),
            adaptation = dim(67.0),
            overallScore = 66.5,
            overallConfidence = 0.78,
            percentileVsCohort = 0.62,
            generatedBy = "progress-engine-v2.3.1",
        )

        assertEquals("rolling_30d", snap.window)
        assertEquals(66.5, snap.overallScore, 0.0)
        assertEquals(0.62, snap.percentileVsCohort!!, 0.0)
        assertEquals("up", snap.braking.trend14d)
    }

    @Test
    fun skill_dimension_allows_null_last_evidence() {
        val d = SkillDimension(
            score = 50.0,
            confidence = 0.5,
            trend14d = "flat",
            sampleCount = 0,
        )
        assertNull(d.lastEvidenceSessionId)
    }
}
