# ftv-features

Player identity and the feature-store contract.

- `ftv_features.schema` — player, external id, feature snapshot, and prediction records.
- `ftv_features.store` — `FeatureStore` protocol and an in-memory implementation. Postgres is represented by the SQL migration, not by a live driver.
- `migrations/001_init.sql` — tables for `players`, `player_external_ids`, `features_snapshot`, and `predictions`.

External id providers shipped here are `football_api`, `clubelo`, and `manual`. Domestic league is one of the Big 5. Champions League participation belongs in feature payload later, not in the league column.

Valuation labels are not part of this package.
