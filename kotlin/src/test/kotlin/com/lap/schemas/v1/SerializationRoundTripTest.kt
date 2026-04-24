package com.lap.schemas.v1

import kotlinx.serialization.encodeToString
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * T038 contract: every schema type round-trips through kotlinx-
 * serialization byte-identical. Uses the shared [LapSchemasJson]
 * instance (snake_case naming strategy + unknown-key tolerance) so
 * Pydantic JSON payloads deserialize without surprise.
 */
class SerializationRoundTripTest {
    private inline fun <reified T : Any> roundTrip(value: T, expectedSubstring: String? = null): T {
        val json = LapSchemasJson.encodeToString(value)
        if (expectedSubstring != null) {
            assertTrue(
                "expected '$expectedSubstring' in payload, got: $json",
                json.contains(expectedSubstring),
            )
        }
        return LapSchemasJson.decodeFromString(json)
    }

    @Test
    fun source_tag_serializes_as_wire_literal() {
        assertEquals(SourceTag.IRACING, roundTrip(SourceTag.IRACING, "\"iracing\""))
        assertEquals(SourceTag.REAL, roundTrip(SourceTag.REAL, "\"real\""))
        assertEquals(SourceTag.F1_GAME, roundTrip(SourceTag.F1_GAME, "\"f1_game\""))
    }

    @Test
    fun environment_tag_serializes_as_wire_literal() {
        assertEquals(
            EnvironmentTag.REAL_TRACK_DAY,
            roundTrip(EnvironmentTag.REAL_TRACK_DAY, "\"real_track_day\""),
        )
    }

    @Test
    fun weakness_category_serializes_as_wire_literal() {
        assertEquals(
            WeaknessCategory.SETUP_SENSITIVITY,
            roundTrip(WeaknessCategory.SETUP_SENSITIVITY, "\"setup_sensitivity\""),
        )
    }

    @Test
    fun telemetry_sample_round_trips_with_snake_case_timestamps() {
        val sample = TelemetrySample(
            tSourceNs = 1_000_000L,
            tCanonicalNs = 1_000_500L,
            tSourceClock = "racebox_gnss",
            channels = mapOf("speed_mps" to 41.2),
        )
        assertEquals(sample, roundTrip(sample, "\"t_canonical_ns\":1000500"))
    }

    @Test
    fun data_quality_round_trips() {
        val dq = DataQuality(
            score = 92.5,
            gpsFixQuality = 0.98,
            gpsSatelliteCountAvg = 11,
            channelCompleteness = 99.2,
            sampleGapsCount = 2,
            sampleRateStability = 0.95,
            warnings = listOf("gnss_loss_3s"),
            recommendations = emptyList(),
            usableForOverlays = true,
            usableForLongTermCoaching = true,
        )
        val json = LapSchemasJson.encodeToString(dq)
        assertTrue(json.contains("\"gps_fix_quality\":0.98"))
        assertTrue(json.contains("\"usable_for_overlays\":true"))
        assertEquals(dq, LapSchemasJson.decodeFromString<DataQuality>(json))
    }

    @Test
    fun sensor_config_snapshot_round_trips() {
        val snap = SensorConfigSnapshot(
            sensors = listOf(
                SensorConfig(name = "gnss", sampleRateHz = 10.0),
                SensorConfig(name = "accel", sampleRateHz = 50.0, enabled = false),
            ),
            hardwareId = "pixel-8",
        )
        assertEquals(snap, roundTrip(snap, "\"sample_rate_hz\":10.0"))
    }

    @Test
    fun lap_record_round_trips() {
        val lap = LapRecord(
            id = "id-1",
            sessionId = "sess-1",
            lapNumber = 4,
            timeMs = 98_400,
            sectorTimesMs = listOf(32_000, 33_100, 33_300),
            flags = listOf("personal_best"),
        )
        assertEquals(lap, roundTrip(lap, "\"lap_number\":4"))
    }

    @Test
    fun session_manifest_round_trips() {
        val manifest = SessionManifest(
            sessionId = "sess-1",
            driverId = "drv-1",
            bundleVersion = "v2",
            captureApp = "lap-mobile-android",
            captureAppVersion = "0.1.0",
            deviceModel = "Pixel 8",
            deviceOs = "android",
            deviceOsVersion = "14",
            source = SourceTag.REAL,
            carId = "car-1",
            trackId = "track-1",
            trackLayout = "gp",
            environmentTag = EnvironmentTag.REAL_TRACK_DAY,
            startedAt = "2026-04-24T09:00:00Z",
            endedAt = "2026-04-24T09:45:00Z",
            durationSeconds = 2700.0,
            telemetryChecksums = mapOf("telemetry.csv" to "sha256:abc"),
            totalSamples = 27_000,
            sampleRateHz = 10.0,
            dataQuality = DataQuality(
                score = 100.0,
                channelCompleteness = 100.0,
                sampleGapsCount = 0,
                sampleRateStability = 1.0,
                usableForOverlays = true,
                usableForLongTermCoaching = true,
            ),
            sensorConfig = SensorConfigSnapshot(),
        )
        val json = LapSchemasJson.encodeToString(manifest)
        assertTrue(json.contains("\"session_id\":\"sess-1\""))
        assertTrue(json.contains("\"capture_app\":\"lap-mobile-android\""))
        assertTrue(json.contains("\"environment_tag\":\"real_track_day\""))
        assertEquals(manifest, LapSchemasJson.decodeFromString<SessionManifest>(json))
    }

    @Test
    fun weakness_episode_round_trips() {
        val ep = WeaknessEpisode(
            id = "ep-1",
            driverId = "drv-1",
            category = WeaknessCategory.TECHNIQUE,
            subcategory = "trail_brake",
            firstObservedAt = "2026-04-01T10:00:00Z",
            lastObservedAt = "2026-04-23T15:00:00Z",
            recurrenceCount = 4,
            severity = "high",
            confidence = 0.82,
            status = "open",
            libraryRuleId = "R1",
            environmentScope = listOf(EnvironmentTag.REAL_TRACK_DAY),
        )
        assertEquals(ep, roundTrip(ep, "\"library_rule_id\":\"R1\""))
    }

    @Test
    fun action_prescription_round_trips() {
        val rx = ActionPrescription(
            id = "rx-1",
            driverId = "drv-1",
            createdAt = "2026-04-24T09:00:00Z",
            priority = "p0",
            title = "Fix trail brake",
            rationale = "...",
            expectedContext = SessionContext(
                carId = "car-1",
                trackId = "track-1",
                trackLayout = "gp",
            ),
            successCondition = SuccessCondition(
                metric = "m",
                targetValue = 1.0,
                comparison = "gte",
                measurementWindow = "next_session",
            ),
            status = "proposed",
        )
        assertEquals(rx, roundTrip(rx, "\"expected_context\""))
    }

    @Test
    fun coaching_insight_round_trips() {
        val insight = CoachingInsight(
            id = "i-1",
            sessionId = "s-1",
            driverId = "d-1",
            observation = "o",
            likelyCause = "c",
            action = "a",
            confidence = 0.7,
            severity = "MED",
            displayLevel = "INTERMEDIATE",
        )
        assertEquals(insight, roundTrip(insight, "\"likely_cause\":\"c\""))
    }

    @Test
    fun driver_progress_snapshot_round_trips_and_renames_trend_14d() {
        val dim = SkillDimension(score = 70.0, confidence = 0.8, trend14d = "up", sampleCount = 10)
        val snap = DriverProgressSnapshot(
            id = "snap-1",
            driverId = "drv-1",
            capturedAt = "2026-04-24T10:00:00Z",
            window = "rolling_30d",
            windowStart = "2026-03-25T00:00:00Z",
            windowEnd = "2026-04-24T00:00:00Z",
            braking = dim,
            throttlePickup = dim,
            minimumSpeed = dim,
            lineConsistency = dim,
            tireManagement = dim,
            racecraft = dim,
            fatigueConsistency = dim,
            strategyExecution = dim,
            setupSensitivity = dim,
            adaptation = dim,
            overallScore = 66.0,
            overallConfidence = 0.78,
            generatedBy = "engine-v1",
        )
        val json = LapSchemasJson.encodeToString(snap)
        assertTrue(
            "expected explicit trend_14d rename, got: $json",
            json.contains("\"trend_14d\":\"up\""),
        )
        assertEquals(snap, LapSchemasJson.decodeFromString<DriverProgressSnapshot>(json))
    }
}
