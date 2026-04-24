package com.lap.schemas.v1

/**
 * UUIDv7 as a String alias. Kept a typealias — not a value class — so
 * all the schema data classes stay cheap (no per-field boxing), and
 * kotlinx-serialization round-trips them as plain strings on the wire.
 *
 * Validation happens explicitly via [validateUuid7] at trust boundaries
 * (file load, network deserialize, user-supplied fields). Mirrors
 * Pydantic's `Annotated[UUID, AfterValidator(_validate_uuid7)]`.
 */
typealias UUID7 = String

private val UUID7_REGEX: Regex = Regex(
    pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$",
    option = RegexOption.IGNORE_CASE,
)

/**
 * Returns [value] if it is a well-formed UUIDv7 (canonical 8-4-4-4-12
 * hex with `7` in the version nibble per RFC 9562). Throws
 * [IllegalArgumentException] otherwise — called at trust boundaries,
 * not inside hot paths.
 */
fun validateUuid7(value: String): UUID7 {
    require(UUID7_REGEX.matches(value)) { "Not a UUIDv7: '$value'" }
    return value
}
