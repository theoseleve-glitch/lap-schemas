from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator


def _validate_uuid7(value: UUID) -> UUID:
    if value.version != 7:
        msg = f"expected UUID version 7, got version {value.version}"
        raise ValueError(msg)
    return value


UUID7 = Annotated[UUID, AfterValidator(_validate_uuid7)]
