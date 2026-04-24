package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Verifies the SessionManifest stub can be imported and constructed with
 * fields mirroring the Pydantic source (`lap_schemas.v1.session`). T028–T037
 * refine individual field types; this test only locks the shape.
 */
class SessionManifestTest {
    @Test
    fun can_construct_session_manifest_with_minimum_required_fields() {
        val manifest = SessionManifest(
            sessionId = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaaa",
            driverId = "0194bbbb-bbbb-7bbb-bbbb-bbbbbbbbbbbb",
            bundleVersion = "v2",
            captureApp = "lap-mobile-android",
            captureAppVersion = "0.1.0",
            deviceModel = "Pixel 8",
            deviceOs = "android",
            deviceOsVersion = "14",
            source = "real",
            carId = "0194cccc-cccc-7ccc-cccc-cccccccccccc",
            trackId = "0194dddd-dddd-7ddd-dddd-dddddddddddd",
            trackLayout = "gp",
            environmentTag = "real_track_day",
            startedAt = "2026-04-24T09:00:00Z",
            endedAt = "2026-04-24T09:45:00Z",
            durationSeconds = 2700.0,
            telemetryChecksums = mapOf("telemetry.csv" to "sha256:abc"),
            totalSamples = 27000,
            sampleRateHz = 10.0,
            dataQuality = DataQuality(),
            sensorConfig = SensorConfigSnapshot(),
        )

        assertEquals("v2", manifest.bundleVersion)
        assertEquals("lap-mobile-android", manifest.captureApp)
        assertEquals(27000, manifest.totalSamples)
    }
}
