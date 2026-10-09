"""Training plan for position-specific Δ market-value models.

``plan`` describes the models. It does not read files, query a database, or fit
anything. Labels stay unwired until a licensed valuation feed exists.
"""

from dataclasses import dataclass

POSITIONS: tuple[str, ...] = ("GK", "DF", "MF", "FW")
HORIZON_MONTHS = 6
TARGET = "delta_market_value_eur"


@dataclass(frozen=True)
class PositionModelSpec:
    position: str
    target: str = TARGET
    outputs: tuple[str, ...] = ("direction", "magnitude")
    horizon_months: int = HORIZON_MONTHS


@dataclass(frozen=True)
class TrainingPlan:
    horizon_months: int
    models: tuple[PositionModelSpec, ...]
    label_source: str
    notes: str


class TrainingPipeline:
    """Offline entry point. Calling ``plan`` has no side effects."""

    def plan(self) -> TrainingPlan:
        return TrainingPlan(
            horizon_months=HORIZON_MONTHS,
            models=tuple(PositionModelSpec(position=position) for position in POSITIONS),
            label_source="unconfigured",
            notes=(
                "Labels must come from a licensed valuation feed. "
                "This pipeline does not load data and does not train."
            ),
        )
