from typing import get_args

import pytest
from pydantic import BaseModel, ValidationError

from lap_schemas.v1.source import SourceTag

EXPECTED = frozenset(
    {
        "iracing",
        "acc",
        "ac",
        "ams2",
        "rf2",
        "lmu",
        "rennsport",
        "f1_game",
        "real",
    }
)


def test_source_tag_values_frozen() -> None:
    actual = frozenset(get_args(SourceTag))
    assert actual == EXPECTED


def test_source_tag_accepts_valid_value() -> None:
    class M(BaseModel):
        source: SourceTag

    m = M(source="iracing")
    assert m.source == "iracing"


def test_source_tag_rejects_unknown_value() -> None:
    class M(BaseModel):
        source: SourceTag

    with pytest.raises(ValidationError):
        M(**{"source": "unknown_sim"})
