package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Locks the WeaknessEpisode shape mirroring
 * `lap_schemas.v1.weakness_episode`. Consumer-side: the mobile app
 * renders episodes the backend produced (coaching intelligence is
 * server-owned per ADR-012); this type exists so the InsightCache
 * (T045) can cache them for offline view.
 */
class WeaknessEpisodeTest {
    @Test
    fun can_build_open_episode_with_backend_linkage() {
        val episode = WeaknessEpisode(
            id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa1",
            driverId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            category = WeaknessCategory.TECHNIQUE,
            subcategory = "trail_braking_release",
            environmentScope = listOf(EnvironmentTag.REAL_TRACK_DAY, EnvironmentTag.SIM_PRACTICE),
            firstObservedAt = "2026-04-01T10:00:00Z",
            lastObservedAt = "2026-04-23T15:12:00Z",
            recurrenceCount = 4,
            sessionsAffected = listOf(
                "0194cccc-cccc-7ccc-cccc-cccccccccccc",
                "0194dddd-dddd-7ddd-dddd-dddddddddddd",
            ),
            severity = "high",
            confidence = 0.82,
            status = "open",
            libraryRuleId = "TRAIL_BRAKING_RELEASE_001",
        )

        assertEquals(WeaknessCategory.TECHNIQUE, episode.category)
        assertEquals(4, episode.recurrenceCount)
        assertEquals("high", episode.severity)
        assertNull(episode.resolvedAt)
        assertEquals(0.02, episode.confidenceDecayPerDay, 0.0)
    }

    @Test
    fun six_weakness_categories_present() {
        val wire = WeaknessCategory.entries.map { it.wireValue }.toSet()
        assertEquals(
            setOf(
                "technique",
                "consistency",
                "setup_sensitivity",
                "confidence",
                "race_management",
                "execution",
            ),
            wire,
        )
    }

    @Test
    fun resolved_episode_carries_timestamp_and_empty_default_links() {
        val episode = WeaknessEpisode(
            id = "0194eeee-eeee-7eee-eeee-eeeeeeeeeeee",
            driverId = "0194ffff-ffff-7fff-ffff-ffffffffffff",
            category = WeaknessCategory.EXECUTION,
            subcategory = "launch_rpm_drop",
            firstObservedAt = "2026-03-01T09:00:00Z",
            lastObservedAt = "2026-04-15T10:00:00Z",
            recurrenceCount = 0,
            severity = "low",
            confidence = 0.1,
            status = "resolved",
            resolvedAt = "2026-04-20T12:00:00Z",
            libraryRuleId = "LAUNCH_RPM_001",
        )
        assertTrue(episode.linkedPrescriptions.isEmpty())
        assertTrue(episode.linkedInsights.isEmpty())
        assertTrue(episode.environmentScope.isEmpty())
        assertEquals("2026-04-20T12:00:00Z", episode.resolvedAt)
    }
}
