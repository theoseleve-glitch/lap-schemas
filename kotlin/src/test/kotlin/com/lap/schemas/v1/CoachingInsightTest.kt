package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/**
 * Locks the CoachingInsight stub shape. No Pydantic source exists yet
 * (see KDoc on [CoachingInsight]); this stub is the mobile-facing
 * subset: what the dashboard + InsightCache (T045) actually render.
 */
class CoachingInsightTest {
    @Test
    fun can_build_displayable_insight() {
        val insight = CoachingInsight(
            id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa1",
            sessionId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            driverId = "0194cccc-cccc-7ccc-cccc-cccccccccccc",
            observation = "late apex at T4 on 6 of 10 laps",
            likelyCause = "steering input saturated before clipping point",
            action = "shift 5m earlier on the straight; hold the line through mid-corner",
            confidence = 0.74,
            severity = "MED",
            displayLevel = "INTERMEDIATE",
        )

        assertEquals("MED", insight.severity)
        assertEquals("INTERMEDIATE", insight.displayLevel)
        assertNull(insight.reviewLaterAt)
        assertNull(insight.createdAt)
    }

    @Test
    fun optional_timestamps_may_be_populated() {
        val insight = CoachingInsight(
            id = "0194dddd-dddd-7ddd-dddd-dddddddddddd",
            sessionId = "0194eeee-eeee-7eee-eeee-eeeeeeeeeeee",
            driverId = "0194ffff-ffff-7fff-ffff-ffffffffffff",
            observation = "inconsistent brake release",
            likelyCause = "muscle memory not yet calibrated",
            action = "three focused laps on release timing",
            confidence = 0.55,
            severity = "LOW",
            displayLevel = "BEGINNER",
            reviewLaterAt = "2026-05-01T12:00:00Z",
            createdAt = "2026-04-24T10:00:00Z",
        )
        assertEquals("2026-05-01T12:00:00Z", insight.reviewLaterAt)
        assertEquals("2026-04-24T10:00:00Z", insight.createdAt)
    }
}
