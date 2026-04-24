import pytest

from lap_schemas.v1.weakness_category import WeaknessCategory

EXPECTED = frozenset(
    {
        "technique",
        "consistency",
        "setup_sensitivity",
        "confidence",
        "race_management",
        "execution",
    }
)


def test_weakness_category_values_frozen() -> None:
    actual = frozenset(member.value for member in WeaknessCategory)
    assert actual == EXPECTED


def test_weakness_category_has_exactly_six_members() -> None:
    assert len(list(WeaknessCategory)) == 6


def test_weakness_category_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match="'bogus'"):
        WeaknessCategory("bogus")
