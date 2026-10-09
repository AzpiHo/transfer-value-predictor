from datetime import date
from uuid import UUID

import pytest
from pydantic import ValidationError

from ftv_features import (
    FeatureSnapshot,
    IdProvider,
    League,
    MemoryFeatureStore,
    Player,
    PlayerExternalId,
    Position,
)

PLAYER_ID = UUID("11111111-1111-4111-8111-111111111111")


def test_player_round_trip() -> None:
    player = Player(
        id=PLAYER_ID,
        display_name="Sample Keeper",
        primary_position=Position.GK,
        league=League.EPL,
    )
    assert player.model_dump()["league"] == "EPL"


def test_rejects_unknown_position() -> None:
    with pytest.raises(ValidationError):
        Player(
            id=PLAYER_ID,
            display_name="Sample Keeper",
            primary_position="ST",  # type: ignore[arg-type]
        )


def test_external_id_providers() -> None:
    row = PlayerExternalId(
        player_id=PLAYER_ID,
        provider=IdProvider.CLUBELO,
        external_id="sample-fc",
    )
    assert row.provider is IdProvider.CLUBELO


def test_memory_store_keeps_latest_snapshot() -> None:
    store = MemoryFeatureStore()
    older = FeatureSnapshot(
        player_id=PLAYER_ID,
        as_of=date(2026, 1, 1),
        payload={"minutes": 900},
        source="stub",
    )
    newer = FeatureSnapshot(
        player_id=PLAYER_ID,
        as_of=date(2026, 4, 1),
        payload={"minutes": 1400},
        source="stub",
    )
    store.put_snapshot(newer)
    store.put_snapshot(older)
    latest = store.latest_snapshot(PLAYER_ID)
    assert latest is not None
    assert latest.as_of == date(2026, 4, 1)


def test_memory_store_rejects_other_horizons() -> None:
    store = MemoryFeatureStore()
    with pytest.raises(ValueError):
        store.put_snapshot(
            FeatureSnapshot(
                player_id=PLAYER_ID,
                as_of=date(2026, 4, 1),
                horizon_months=12,
                payload={},
                source="stub",
            )
        )
