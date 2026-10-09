"""Keep the duplicated scope constants aligned across packages."""

from ftv_features.scope import CONTINENTAL, HORIZON_MONTHS, LEAGUES, POSITIONS
from ftv_ingest.football_api import BIG_5_AND_UCL
from ftv_ml.pipeline import HORIZON_MONTHS as ML_HORIZON
from ftv_ml.pipeline import POSITIONS as ML_POSITIONS


def test_competitions_match_feature_scope() -> None:
    league_ids = [item.id for item in BIG_5_AND_UCL if item.kind == "league"]
    continental_ids = [item.id for item in BIG_5_AND_UCL if item.kind == "continental"]
    assert tuple(league_ids) == LEAGUES
    assert tuple(continental_ids) == CONTINENTAL


def test_training_scope_matches_feature_store() -> None:
    assert ML_POSITIONS == POSITIONS
    assert ML_HORIZON == HORIZON_MONTHS == 6
