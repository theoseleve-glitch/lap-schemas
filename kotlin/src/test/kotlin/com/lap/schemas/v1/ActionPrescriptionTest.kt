package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/**
 * Locks the ActionPrescription shape mirroring
 * `lap_schemas.v1.action_prescription`. Backend-generated, mobile-
 * consumed (ADR-012: no local prescription logic). Cached in
 * PrescriptionCacheEntity (T046) for offline view.
 */
class ActionPrescriptionTest {
    @Test
    fun can_build_proposed_prescription() {
        val rx = ActionPrescription(
            id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa1",
            driverId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            createdAt = "2026-04-24T09:00:00Z",
            priority = "p0",
            title = "Consistent trail-brake release at T4",
            rationale = "3 consecutive sessions show late release -> understeer.",
            expectedContext = SessionContext(
                carId = "0194cccc-cccc-7ccc-cccc-cccccccccccc",
                trackId = "0194dddd-dddd-7ddd-dddd-dddddddddddd",
                trackLayout = "gp",
                environmentTag = EnvironmentTag.REAL_TRACK_DAY,
            ),
            successCondition = SuccessCondition(
                metric = "t4_release_slope",
                targetValue = -0.25,
                comparison = "lte",
                measurementWindow = "next_3_sessions",
            ),
            status = "proposed",
        )

        assertEquals("p0", rx.priority)
        assertEquals("proposed", rx.status)
        assertNull(rx.weaknessEpisodeId)
        assertNull(rx.acceptedAt)
        assertNull(rx.outcomeId)
    }

    @Test
    fun session_context_defaults_optional_fields_to_null() {
        val ctx = SessionContext(
            carId = "0194cccc-cccc-7ccc-cccc-cccccccccccc",
            trackId = "0194dddd-dddd-7ddd-dddd-dddddddddddd",
            trackLayout = "gp",
        )
        assertNull(ctx.environmentTag)
        assertNull(ctx.conditions)
    }

    @Test
    fun success_condition_target_pct_defaults_null() {
        val cond = SuccessCondition(
            metric = "apex_speed_mps",
            targetValue = 28.0,
            comparison = "gte",
            measurementWindow = "next_session",
        )
        assertNull(cond.targetPct)
    }
}
