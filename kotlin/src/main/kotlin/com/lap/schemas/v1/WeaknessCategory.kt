package com.lap.schemas.v1

/**
 * Top-level weakness category, mirroring
 * `lap_schemas.v1.weakness_category.WeaknessCategory` (Python StrEnum).
 * Shared by [WeaknessEpisode] and the library rule registry. @SerialName
 * wiring lands in T038.
 */
enum class WeaknessCategory(val wireValue: String) {
    TECHNIQUE("technique"),
    CONSISTENCY("consistency"),
    SETUP_SENSITIVITY("setup_sensitivity"),
    CONFIDENCE("confidence"),
    RACE_MANAGEMENT("race_management"),
    EXECUTION("execution"),
    ;

    companion object {
        fun fromWire(value: String): WeaknessCategory =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown WeaknessCategory wire value: '$value'")
    }
}
