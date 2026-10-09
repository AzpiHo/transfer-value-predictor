"""Product scope shared by ingest, training, and the prediction API."""

LEAGUES: tuple[str, ...] = (
    "EPL",
    "LA_LIGA",
    "SERIE_A",
    "BUNDESLIGA",
    "LIGUE_1",
)
CONTINENTAL: tuple[str, ...] = ("UCL",)
POSITIONS: tuple[str, ...] = ("GK", "DF", "MF", "FW")
HORIZON_MONTHS: int = 6
