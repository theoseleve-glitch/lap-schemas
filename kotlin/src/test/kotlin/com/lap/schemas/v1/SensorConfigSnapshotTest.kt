package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Locks the SensorConfigSnapshot shape mirroring
 * `lap_schemas.v1.sensor_config`. Bundled manifest writers (T139)
 * serialise this snapshot so the server knows exactly which sensors
 * produced the telemetry, at what rate, and which hardware serialised
 * them (per-sample provenance requires this metadata).
 */
class SensorConfigSnapshotTest {
    @Test
    fun can_build_snapshot_with_sensors_and_hardware() {
        val snap = SensorConfigSnapshot(
            sensors = listOf(
                SensorConfig(name = "gnss", sampleRateHz = 10.0),
                SensorConfig(name = "accel", sampleRateHz = 50.0, enabled = true),
                SensorConfig(name = "gyro", sampleRateHz = 50.0, enabled = false),
            ),
            hardwareId = "racebox-serial-12345",
            firmwareVersion = "3.4.1",
        )

        assertEquals(3, snap.sensors.size)
        assertEquals("gnss", snap.sensors[0].name)
        assertTrue(snap.sensors[0].enabled)
        assertEquals("racebox-serial-12345", snap.hardwareId)
    }

    @Test
    fun defaults_empty_sensors_and_null_hardware() {
        val snap = SensorConfigSnapshot()
        assertEquals(emptyList<SensorConfig>(), snap.sensors)
        assertNull(snap.hardwareId)
        assertNull(snap.firmwareVersion)
    }

    @Test
    fun sensor_config_enabled_defaults_to_true() {
        val cfg = SensorConfig(name = "barometer", sampleRateHz = 1.0)
        assertTrue(cfg.enabled)
    }
}
