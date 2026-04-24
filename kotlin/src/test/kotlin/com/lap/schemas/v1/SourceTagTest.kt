package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * SourceTag mirrors the `lap_schemas.v1.source.SourceTag` Literal. The
 * wire values are the identifiers server-side ingestion uses — they must
 * stay byte-identical to the Pydantic literal or ingest rejects the
 * manifest (ADR-012).
 */
class SourceTagTest {
    @Test
    fun all_nine_wire_values_are_present() {
        val wire = SourceTag.entries.map { it.wireValue }.toSet()
        assertEquals(
            setOf("iracing", "acc", "ac", "ams2", "rf2", "lmu", "rennsport", "f1_game", "real"),
            wire,
        )
    }

    @Test
    fun from_wire_round_trips() {
        for (tag in SourceTag.entries) {
            assertEquals(tag, SourceTag.fromWire(tag.wireValue))
        }
    }

    @Test(expected = IllegalArgumentException::class)
    fun from_wire_rejects_unknown() {
        SourceTag.fromWire("assetto_corsa_2")
    }
}
