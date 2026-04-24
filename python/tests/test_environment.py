import pytest

from lap_schemas.v1.environment import EnvironmentTag

EXPECTED = frozenset(
    {
        "sim_practice",
        "sim_race",
        "real_track_day",
        "real_race",
        "real_karting",
        "drill",
        "test",
    }
)


def test_environment_tag_values_frozen() -> None:
    actual = frozenset(member.value for member in EnvironmentTag)
    assert actual == EXPECTED


def test_environment_tag_has_exactly_seven_members() -> None:
    assert len(list(EnvironmentTag)) == 7


def test_environment_tag_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match="'unknown'"):
        EnvironmentTag("unknown")
