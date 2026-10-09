"""Deterministic mocked predictions.

The digest picks a direction and a magnitude on a 50,000-euro grid.
It is stable across processes. It is not a model.
"""

import hashlib

from ftv_api.schemas import Direction, Prediction, Scope

MODEL_VERSION = "stub-0.1.0"
LEAGUES = ["EPL", "LA_LIGA", "SERIE_A", "BUNDESLIGA", "LIGUE_1"]
COMPETITIONS = ["UCL"]


def mock_delta(player_id: str) -> tuple[Direction, int]:
    digest = int(hashlib.sha256(player_id.encode("utf-8")).hexdigest()[:8], 16)
    bucket = digest % 5
    if bucket == 0:
        return Direction.FLAT, 0
    magnitude = ((digest // 5) % 160 + 1) * 50_000
    if bucket in (1, 2):
        return Direction.UP, magnitude
    return Direction.DOWN, -magnitude


def mock_prediction(player_id: str) -> Prediction:
    direction, delta = mock_delta(player_id)
    return Prediction(
        player_id=player_id,
        horizon_months=6,
        direction=direction,
        delta_value_eur=delta,
        model_version=MODEL_VERSION,
        scope=Scope(leagues=LEAGUES, competitions=COMPETITIONS, horizon_months=6),
        label_source="unconfigured",
        mocked=True,
    )
