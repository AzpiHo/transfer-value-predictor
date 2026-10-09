"""Provider-agnostic football data client.

The shipped adapter is ``stub``. It knows the competition scope and returns
no players. It does not open sockets. Paid providers are optional future
adapters behind ``build_football_client``; this package does not select or
call one.

Valuation websites are out of scope. Do not add a client for them.
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Competition:
    id: str
    name: str
    kind: str


BIG_5_AND_UCL: tuple[Competition, ...] = (
    Competition("EPL", "Premier League", "league"),
    Competition("LA_LIGA", "La Liga", "league"),
    Competition("SERIE_A", "Serie A", "league"),
    Competition("BUNDESLIGA", "Bundesliga", "league"),
    Competition("LIGUE_1", "Ligue 1", "league"),
    Competition("UCL", "UEFA Champions League", "continental"),
)


@dataclass(frozen=True)
class PlayerRef:
    provider: str
    external_id: str
    display_name: str
    competition_id: str


class FootballApiClient(Protocol):
    provider: str

    def list_competitions(self) -> list[Competition]:
        """Competitions in product scope."""

    def list_player_refs(self, competition_id: str) -> list[PlayerRef]:
        """External player refs for one competition. May be empty."""


class StubFootballApiClient:
    """Offline stand-in. ``provider`` is always ``stub``."""

    provider = "stub"

    def list_competitions(self) -> list[Competition]:
        return list(BIG_5_AND_UCL)

    def list_player_refs(self, competition_id: str) -> list[PlayerRef]:
        known = {competition.id for competition in BIG_5_AND_UCL}
        if competition_id not in known:
            raise KeyError(competition_id)
        return []


def build_football_client(provider: str) -> FootballApiClient:
    """Return the client for ``FOOTBALL_API_PROVIDER``.

    Anything other than ``stub`` is rejected. No HTTP client is constructed.
    """

    if provider == "stub":
        return StubFootballApiClient()
    raise NotImplementedError(
        f"Football API provider {provider!r} is not wired. "
        "Paid providers are optional future work. Use FOOTBALL_API_PROVIDER=stub."
    )
