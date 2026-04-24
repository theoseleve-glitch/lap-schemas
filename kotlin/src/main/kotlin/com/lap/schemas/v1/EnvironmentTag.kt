package com.lap.schemas.v1

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Session environment, promoted to a typed enum from the String stub
 * that T027 carried on [SessionManifest.environmentTag]. Wire values
 * match `lap_schemas.v1.environment.EnvironmentTag` byte-for-byte.
 */
@Serializable
enum class EnvironmentTag(val wireValue: String) {
    @SerialName("sim_practice") SIM_PRACTICE("sim_practice"),
    @SerialName("sim_race") SIM_RACE("sim_race"),
    @SerialName("real_track_day") REAL_TRACK_DAY("real_track_day"),
    @SerialName("real_race") REAL_RACE("real_race"),
    @SerialName("real_karting") REAL_KARTING("real_karting"),
    @SerialName("drill") DRILL("drill"),
    @SerialName("test") TEST("test"),
    ;

    companion object {
        fun fromWire(value: String): EnvironmentTag =
            entries.firstOrNull { it.wireValue == value }
                ?: throw IllegalArgumentException("Unknown EnvironmentTag wire value: '$value'")
    }
}
