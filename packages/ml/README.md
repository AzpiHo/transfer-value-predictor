# ftv-ml

Offline training stub for six-month change in player market value.

## Target

`delta_market_value_eur` over a horizon of **6 months**, reported as:

- **direction** — `up`, `down`, or `flat`
- **magnitude** — signed euros (flat is `0`)

The product covers the Big 5 leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1) and the UEFA Champions League.

## Position-specific models

Goalkeepers, defenders, midfielders, and forwards do not share one fit. `TrainingPipeline.plan()` returns four model specs:

| Position | Code |
| --- | --- |
| Goalkeeper | `GK` |
| Defender | `DF` |
| Midfielder | `MF` |
| Forward | `FW` |

Each spec names the same target and the same two outputs. No model is fit in this package. There is no training loop, no feature matrix loader, and no artifact writer.

## Legal label sources

Market-value labels are **not wired**. `label_source` is `unconfigured`.

When labels are added, they must come from a source the project has a right to store and learn from, for example:

- a commercially licensed valuation feed under contract
- a club or league data-sharing agreement
- another feed with explicit redistribution and modelling rights

Never train on scraped Transfermarkt values. Never add scraped valuation tables, pages, or dumps to this package. A notebook placed under `notebooks/` may only call `TrainingPipeline.plan()` until a legal label source exists.

## Run the stub

```bash
python -c "from ftv_ml import TrainingPipeline; print(TrainingPipeline().plan())"
```
