package com.lap.schemas.v1

import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonNamingStrategy

/**
 * Shared [Json] instance configured to round-trip lap-schemas v1 types
 * byte-for-byte against the Pydantic source. `SnakeCase` maps Kotlin
 * camelCase property names to the Pydantic snake_case wire names;
 * the handful of fields where the mapping isn't mechanical (e.g.
 * `trend14d` -> `trend_14d`) carry an explicit `@SerialName`.
 *
 * `ignoreUnknownKeys = true` so forward-compat fields added
 * server-side don't break the mobile parser; `encodeDefaults = false`
 * keeps the wire payload minimal (Pydantic emits defaults, but
 * round-trip equality still holds since the deserializer fills them).
 */
@OptIn(ExperimentalSerializationApi::class)
val LapSchemasJson: Json = Json {
    namingStrategy = JsonNamingStrategy.SnakeCase
    ignoreUnknownKeys = true
    encodeDefaults = true
}
