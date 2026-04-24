package com.lap.schemas.v1

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Top-level weakness category, mirroring
 * `lap_schemas.v1.weakness_category.WeaknessCategory` (Python StrEnum).
 * Shared by [WeaknessEpisode] and the library rule registry.
 */
@Serializable
enum class WeaknessCategory(val wireValue: String) {
    @SerialName("technique") TECHNIQUE("technique"),
    @SerialName("consistency") CONSISTENCY("consistency"),
    @SerialName("setup_sensitivity") SETUP_SENSITIVITY("setup_sensitivity"),
    @SerialName("confidence") CONFIDENCE("confidence"),
    @SerialName("race_management") RACE_MANAGEMENT("race_management"),
    @SerialName("execution") EXECUTION("execution"),
    ;

    companion object {
        fun fromWire(value: String): WeaknessCategory =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown WeaknessCategory wire value: '$value'")
    }
}
