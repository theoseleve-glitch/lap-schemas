package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * EnvironmentTag mirrors the `lap_schemas.v1.environment.EnvironmentTag`
 * Python StrEnum. Wire values must stay byte-identical to the server
 * source (ADR-012).
 */
class EnvironmentTagTest {
    @Test
    fun all_seven_wire_values_are_present() {
        val wire = EnvironmentTag.entries.map { it.wireValue }.toSet()
        assertEquals(
            setOf(
                "sim_practice",
                "sim_race",
                "real_track_day",
                "real_race",
                "real_karting",
                "drill",
                "test",
            ),
            wire,
        )
    }

    @Test
    fun from_wire_round_trips() {
        for (tag in EnvironmentTag.entries) {
            assertEquals(tag, EnvironmentTag.fromWire(tag.wireValue))
        }
    }

    @Test(expected = IllegalArgumentException::class)
    fun from_wire_rejects_unknown() {
        EnvironmentTag.fromWire("race_weekend")
    }
}
