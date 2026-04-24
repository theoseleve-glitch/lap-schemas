from enum import StrEnum


class EnvironmentTag(StrEnum):
    SIM_PRACTICE = "sim_practice"
    SIM_RACE = "sim_race"
    REAL_TRACK_DAY = "real_track_day"
    REAL_RACE = "real_race"
    REAL_KARTING = "real_karting"
    DRILL = "drill"
    TEST = "test"
