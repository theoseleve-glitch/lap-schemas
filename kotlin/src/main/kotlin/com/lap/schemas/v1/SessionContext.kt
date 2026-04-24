package com.lap.schemas.v1

import kotlinx.serialization.Serializable

/**
 * The "where / when / in what conditions" a prescription is intended
 * to be satisfied in. Mirrors `lap_schemas.v1.session_context`.
 * Shared by [ActionPrescription] and any other insight payload that
 * needs to scope itself to a car+track context.
 */
@Serializable
data class SessionContext(
    val carId: UUID7,
    val trackId: UUID7,
    val trackLayout: String,
    val environmentTag: EnvironmentTag? = null,
    val conditions: String? = null,
)
