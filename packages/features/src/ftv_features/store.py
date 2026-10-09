"""Feature-store interface.

``MemoryFeatureStore`` is for tests and local dry-runs. Postgres persistence
is the SQL migration; a driver is intentionally not included yet.
"""

from typing import Protocol
from uuid import UUID

from ftv_features.schema import FeatureSnapshot


class FeatureStore(Protocol):
    def put_snapshot(self, snapshot: FeatureSnapshot) -> None:
        """Insert or replace the snapshot for a player and as-of date."""

    def latest_snapshot(self, player_id: UUID) -> FeatureSnapshot | None:
        """Return the newest snapshot for a player, if one exists."""


class MemoryFeatureStore:
    def __init__(self) -> None:
        self._rows: dict[tuple[UUID, object, int], FeatureSnapshot] = {}

    def put_snapshot(self, snapshot: FeatureSnapshot) -> None:
        if snapshot.horizon_months != 6:
            raise ValueError("horizon_months must be 6")
        key = (snapshot.player_id, snapshot.as_of, snapshot.horizon_months)
        self._rows[key] = snapshot

    def latest_snapshot(self, player_id: UUID) -> FeatureSnapshot | None:
        matches = [row for (pid, _, _), row in self._rows.items() if pid == player_id]
        if not matches:
            return None
        return max(matches, key=lambda row: row.as_of)
