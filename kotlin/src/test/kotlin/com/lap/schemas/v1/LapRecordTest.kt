package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Locks the LapRecord shape mirroring `lap_schemas.v1.lap_record`.
 * Server-side lap detection (ADR-012) writes these records from raw
 * GPS — mobile consumes them for dashboard overlays and imports them
 * into the offline InsightCache (T045).
 */
class LapRecordTest {
    @Test
    fun can_build_valid_lap_with_sectors() {
        val lap = LapRecord(
            id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa1",
            sessionId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            lapNumber = 3,
            timeMs = 98_412,
            sectorTimesMs = listOf(32_104, 33_287, 33_021),
            flags = listOf("personal_best"),
        )

        assertEquals(3, lap.lapNumber)
        assertEquals(98_412, lap.timeMs)
        assertEquals(listOf(32_104, 33_287, 33_021), lap.sectorTimesMs)
        assertEquals(listOf("personal_best"), lap.flags)
        assertTrue(lap.valid)
    }

    @Test
    fun defaults_valid_true_with_empty_sectors_and_flags() {
        val lap = LapRecord(
            id = "0194cccc-cccc-7ccc-cccc-cccccccccccc",
            sessionId = "0194dddd-dddd-7ddd-dddd-dddddddddddd",
            lapNumber = 0,
        )
        assertNull(lap.timeMs)
        assertEquals(emptyList<Int>(), lap.sectorTimesMs)
        assertEquals(emptyList<String>(), lap.flags)
        assertTrue(lap.valid)
    }

    @Test
    fun can_mark_invalid() {
        val lap = LapRecord(
            id = "0194eeee-eeee-7eee-eeee-eeeeeeeeeeee",
            sessionId = "0194ffff-ffff-7fff-ffff-ffffffffffff",
            lapNumber = 1,
            valid = false,
            flags = listOf("track_limits"),
        )
        assertEquals(false, lap.valid)
    }
}
