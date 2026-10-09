"""Canonical player identity and stored prediction records.

These models describe the feature store. They do not fetch data.
"""

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from ftv_features.scope import HORIZON_MONTHS


class Position(str, Enum):
    GK = "GK"
    DF = "DF"
    MF = "MF"
    FW = "FW"


class League(str, Enum):
    EPL = "EPL"
    LA_LIGA = "LA_LIGA"
    SERIE_A = "SERIE_A"
    BUNDESLIGA = "BUNDESLIGA"
    LIGUE_1 = "LIGUE_1"


class IdProvider(str, Enum):
    """Sources allowed to mint an external id.

    Paid football-API vendors, if added later, still use ``football_api``
    plus ``FOOTBALL_API_PROVIDER`` to name the vendor. ClubElo is separate.
    """

    FOOTBALL_API = "football_api"
    CLUBELO = "clubelo"
    MANUAL = "manual"


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


class Player(BaseModel):
    id: UUID
    display_name: str = Field(min_length=1)
    primary_position: Position
    league: League | None = None
    date_of_birth: date | None = None
    nationality: str | None = None
    current_club: str | None = None


class PlayerExternalId(BaseModel):
    player_id: UUID
    provider: IdProvider
    external_id: str = Field(min_length=1)


class FeatureSnapshot(BaseModel):
    player_id: UUID
    as_of: date
    horizon_months: int = HORIZON_MONTHS
    payload: dict[str, object] = Field(default_factory=dict)
    source: str = Field(min_length=1)


class PredictionRecord(BaseModel):
    player_id: UUID
    as_of: date
    horizon_months: int = HORIZON_MONTHS
    direction: Direction
    delta_value_eur: int
    model_version: str = Field(min_length=1)
    created_at: datetime | None = None
