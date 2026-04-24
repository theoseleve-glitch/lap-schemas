package com.lap.schemas.v1

/**
 * Session environment, promoted to a typed enum from the String stub
 * that T027 carried on [SessionManifest.environmentTag]. Wire values
 * match `lap_schemas.v1.environment.EnvironmentTag` byte-for-byte.
 *
 * @SerialName wiring arrives in T038.
 */
enum class EnvironmentTag(val wireValue: String) {
    SIM_PRACTICE("sim_practice"),
    SIM_RACE("sim_race"),
    REAL_TRACK_DAY("real_track_day"),
    REAL_RACE("real_race"),
    REAL_KARTING("real_karting"),
    DRILL("drill"),
    TEST("test"),
    ;

    companion object {
        fun fromWire(value: String): EnvironmentTag =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown EnvironmentTag wire value: '$value'")
    }
}
