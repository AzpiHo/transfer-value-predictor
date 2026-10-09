"""Response models. FastAPI publishes these on the OpenAPI schema."""

from enum import Enum

from pydantic import BaseModel, Field


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


class Scope(BaseModel):
    leagues: list[str]
    competitions: list[str]
    horizon_months: int = 6


class Health(BaseModel):
    status: str
    service: str


class Prediction(BaseModel):
    player_id: str
    horizon_months: int = Field(description="Fixed product horizon, in months.")
    direction: Direction
    delta_value_eur: int = Field(
        description="Signed magnitude in euros. Flat predictions are 0."
    )
    currency: str = "EUR"
    model_version: str
    scope: Scope
    label_source: str = "unconfigured"
    mocked: bool = True
