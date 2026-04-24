package com.lap.schemas.v1

import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * T039: UUID7 is a String typealias (no runtime wrapping — data classes
 * stay cheap), but a [validateUuid7] helper enforces the RFC 9562
 * version-7 shape at the trust boundary (file load, network deserialize,
 * user input). Mirrors Pydantic's `AfterValidator(_validate_uuid7)`.
 */
class IdsTest {
    @Test
    fun accepts_valid_lowercase_uuid_v7() {
        val id = "0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaaa"
        assertEquals(id, validateUuid7(id))
    }

    @Test
    fun accepts_valid_uppercase_uuid_v7() {
        val id = "0194AAAA-AAAA-7AAA-AAAA-AAAAAAAAAAAA"
        assertEquals(id, validateUuid7(id))
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_version_4_uuid() {
        validateUuid7("0194aaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_wrong_dash_positions() {
        validateUuid7("0194aaaaaaaa-7aaa-aaaa-aaaaaaaaaaaa-aaaa")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_non_hex_characters() {
        validateUuid7("0194aaaa-aaaa-7aaa-aaaa-zzzzzzzzzzzz")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_empty_string() {
        validateUuid7("")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_too_short() {
        validateUuid7("0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaa")
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejects_too_long() {
        validateUuid7("0194aaaa-aaaa-7aaa-aaaa-aaaaaaaaaaaab")
    }
}
