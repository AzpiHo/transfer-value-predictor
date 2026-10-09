from datetime import date

import pytest

from ftv_ingest import (
    BIG_5_AND_UCL,
    ClubEloClient,
    IngestConfig,
    build_football_client,
)


def test_default_config_is_offline() -> None:
    config = IngestConfig.from_env({})
    assert config.football_api_provider == "stub"
    assert config.football_api_key is None
    assert config.clubelo_fetch_enabled is False
    assert config.clubelo_base_url == "http://api.clubelo.com"
    assert config.database_url is None


def test_stub_client_lists_scope_without_players() -> None:
    client = build_football_client("stub")
    ids = [competition.id for competition in client.list_competitions()]
    assert ids == [competition.id for competition in BIG_5_AND_UCL]
    assert client.list_player_refs("EPL") == []
    assert client.list_player_refs("UCL") == []


def test_unknown_competition_is_rejected() -> None:
    client = build_football_client("stub")
    with pytest.raises(KeyError):
        client.list_player_refs("MLS")


def test_paid_provider_is_not_called() -> None:
    with pytest.raises(NotImplementedError):
        build_football_client("api-football")


def test_clubelo_fetch_stays_offline() -> None:
    quiet = ClubEloClient(IngestConfig.from_env({}))
    assert quiet.fetch_ratings(date(2026, 4, 1)) == []

    enabled = ClubEloClient(
        IngestConfig.from_env({"CLUBELO_FETCH_ENABLED": "true"})
    )
    with pytest.raises(NotImplementedError):
        enabled.fetch_ratings(date(2026, 4, 1))
