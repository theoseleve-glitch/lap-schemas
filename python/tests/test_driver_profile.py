import pytest
import uuid6
from pydantic import ValidationError

from lap_schemas.v1.driver_profile import DriverProfile, DriverProfileUpdate


def _example() -> DriverProfile:
    return DriverProfile(
        id=uuid6.uuid7(),
        user_id=uuid6.uuid7(),
        display_name="Theo",
        skill_level="beginner",
        cohort_opt_in=False,
    )


def test_driver_profile_builds() -> None:
    p = _example()
    assert p.display_name == "Theo"
    assert p.skill_level == "beginner"


def test_driver_profile_rejects_invalid_skill_level() -> None:
    with pytest.raises(ValidationError):
        DriverProfile(
            id=uuid6.uuid7(),
            user_id=uuid6.uuid7(),
            display_name="x",
            skill_level="banana",  # type: ignore[arg-type]
            cohort_opt_in=False,
        )


def test_driver_profile_rejects_empty_display_name() -> None:
    with pytest.raises(ValidationError):
        DriverProfile(
            id=uuid6.uuid7(),
            user_id=uuid6.uuid7(),
            display_name="",
            skill_level="beginner",
            cohort_opt_in=False,
        )


def test_driver_profile_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        DriverProfile(
            id=uuid6.uuid7(),
            user_id=uuid6.uuid7(),
            display_name="x",
            skill_level="beginner",
            cohort_opt_in=False,
            unknown="oops",  # type: ignore[call-arg]
        )


def test_driver_profile_update_all_optional() -> None:
    upd = DriverProfileUpdate()
    assert upd.display_name is None
    assert upd.skill_level is None
    assert upd.cohort_opt_in is None


def test_driver_profile_update_partial() -> None:
    upd = DriverProfileUpdate(skill_level="advanced")
    assert upd.display_name is None
    assert upd.skill_level == "advanced"


def test_driver_profile_update_rejects_invalid_skill_level() -> None:
    with pytest.raises(ValidationError):
        DriverProfileUpdate(skill_level="god_tier")  # type: ignore[arg-type]


def test_driver_profile_update_rejects_empty_display_name() -> None:
    with pytest.raises(ValidationError):
        DriverProfileUpdate(display_name="")


def test_driver_profile_update_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        DriverProfileUpdate(unknown_field="oops")  # type: ignore[call-arg]


def test_driver_profile_v1_reexport() -> None:
    from lap_schemas.v1 import DriverProfile as Re
    from lap_schemas.v1 import DriverProfileUpdate as ReUpd

    assert Re is DriverProfile
    assert ReUpd is DriverProfileUpdate
