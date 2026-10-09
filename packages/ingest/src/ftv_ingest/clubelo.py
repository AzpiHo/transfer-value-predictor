"""ClubElo rating stub.

ClubElo publishes a free daily CSV at ``{CLUBELO_BASE_URL}/YYYY-MM-DD``.
This module records that contract and does not request it.
"""

from dataclasses import dataclass
from datetime import date

from ftv_ingest.config import IngestConfig


@dataclass(frozen=True)
class ClubEloRating:
    club: str
    country: str
    elo: float
    as_of: date


class ClubEloClient:
    def __init__(self, config: IngestConfig) -> None:
        self._config = config

    @property
    def base_url(self) -> str:
        return self._config.clubelo_base_url

    def ratings_path(self, as_of: date) -> str:
        """Path a future adapter would request. Not fetched here."""

        return f"{self._config.clubelo_base_url}/{as_of.isoformat()}"

    def fetch_ratings(self, as_of: date) -> list[ClubEloRating]:
        """Return ratings for ``as_of``.

        Disabled (the default, and the CI setting) returns an empty list.
        Enabled raises until an HTTP adapter exists, so a flag flip cannot
        silently hit the network from this stub.
        """

        if not self._config.clubelo_fetch_enabled:
            return []
        raise NotImplementedError(
            f"ClubElo live fetch is not implemented ({self.ratings_path(as_of)}). "
            "This build does not call the network."
        )
