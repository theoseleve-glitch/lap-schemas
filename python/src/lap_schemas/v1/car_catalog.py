"""Car catalog wire schemas (T142 / ADR-014).

Server-curated car catalog exposed to clients. Mirrors
`coaching/catalog/loader.CarCatalogEntry` minus the internal
`source_provider` field.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DriveType = Literal["RWD", "FWD", "AWD"]
Aspiration = Literal["NA", "Turbo", "Supercharged", "Hybrid"]


class CarCatalogPublic(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    master_car_id: str
    name: str
    manufacturer: str
    model: str
    year: int = Field(gt=1900)
    car_class: str
    mass_kg: float = Field(gt=0)
    power_kw: float = Field(gt=0)
    drive_type: DriveType
    aspiration: Aspiration


class CarCatalogList(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    items: tuple[CarCatalogPublic, ...]
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
