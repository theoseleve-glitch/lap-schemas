package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Locks the TelemetrySample stub shape. Dual timestamps (ADR-007) are the
 * reason this type exists: clients ship both the source-clock reading and
 * the canonical-timebase reading so ingest can forensically re-align.
 */
class TelemetrySampleTest {
    @Test
    fun carries_both_source_and_canonical_timestamps() {
        val sample = TelemetrySample(
            tSourceNs = 123_456_789L,
            tCanonicalNs = 123_456_800L,
            tSourceClock = "racebox_gnss",
            channels = mapOf("speed_mps" to 41.3, "lat_g" to 0.85),
        )

        assertEquals(123_456_789L, sample.tSourceNs)
        assertEquals(123_456_800L, sample.tCanonicalNs)
        assertEquals("racebox_gnss", sample.tSourceClock)
        assertEquals(41.3, sample.channels.getValue("speed_mps"), 0.0)
    }

    @Test
    fun channels_default_to_empty() {
        val sample = TelemetrySample(
            tSourceNs = 0L,
            tCanonicalNs = 0L,
            tSourceClock = "gnss",
        )
        assertEquals(emptyMap<String, Double>(), sample.channels)
    }
}
