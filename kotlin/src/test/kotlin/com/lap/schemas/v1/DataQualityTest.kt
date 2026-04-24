package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/**
 * Locks the DataQuality shape mirroring
 * `lap_schemas.v1.data_quality.DataQuality`. The two `usable_for_*`
 * flags are deliberately required (not defaulted): they drive server-side
 * gating for overlays and long-term coaching rollups, so clients must
 * commit to a verdict.
 */
class DataQualityTest {
    @Test
    fun can_construct_with_all_fields() {
        val dq = DataQuality(
            score = 92.5,
            gpsFixQuality = 0.98,
            gpsSatelliteCountAvg = 11,
            channelCompleteness = 99.2,
            sampleGapsCount = 2,
            sampleRateStability = 0.95,
            warnings = listOf("gnss_loss_3s"),
            recommendations = listOf("wait_for_more_sats"),
            usableForOverlays = true,
            usableForLongTermCoaching = true,
        )

        assertEquals(92.5, dq.score, 0.0)
        assertEquals(11, dq.gpsSatelliteCountAvg)
        assertEquals(listOf("gnss_loss_3s"), dq.warnings)
    }

    @Test
    fun optional_fields_default_to_null_and_empty_lists() {
        val dq = DataQuality(
            score = 0.0,
            channelCompleteness = 0.0,
            sampleGapsCount = 0,
            sampleRateStability = 0.0,
            usableForOverlays = false,
            usableForLongTermCoaching = false,
        )

        assertNull(dq.gpsFixQuality)
        assertNull(dq.gpsSatelliteCountAvg)
        assertEquals(emptyList<String>(), dq.warnings)
        assertEquals(emptyList<String>(), dq.recommendations)
    }
}
