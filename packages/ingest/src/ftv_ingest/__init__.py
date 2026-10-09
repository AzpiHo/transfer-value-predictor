"""Ingest stubs. No network calls."""

from ftv_ingest.clubelo import ClubEloClient, ClubEloRating
from ftv_ingest.config import IngestConfig
from ftv_ingest.football_api import (
    BIG_5_AND_UCL,
    Competition,
    FootballApiClient,
    PlayerRef,
    StubFootballApiClient,
    build_football_client,
)

__all__ = [
    "BIG_5_AND_UCL",
    "ClubEloClient",
    "ClubEloRating",
    "Competition",
    "FootballApiClient",
    "IngestConfig",
    "PlayerRef",
    "StubFootballApiClient",
    "build_football_client",
]
