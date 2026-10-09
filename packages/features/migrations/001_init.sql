-- Feature store for 6-month transfer-value predictions.
-- Scope: Big 5 domestic leagues. Champions League is competition context
-- stored later inside features_snapshot.payload, not a league value.
-- External id providers: football_api, clubelo, manual.
-- Valuation labels are not loaded by this migration.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name TEXT NOT NULL,
    date_of_birth DATE,
    primary_position TEXT NOT NULL CHECK (primary_position IN ('GK', 'DF', 'MF', 'FW')),
    nationality TEXT,
    current_club TEXT,
    league TEXT CHECK (
        league IS NULL
        OR league IN ('EPL', 'LA_LIGA', 'SERIE_A', 'BUNDESLIGA', 'LIGUE_1')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE player_external_ids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players (id) ON DELETE CASCADE,
    provider TEXT NOT NULL CHECK (provider IN ('football_api', 'clubelo', 'manual')),
    external_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (provider, external_id)
);

CREATE INDEX player_external_ids_player_id_idx ON player_external_ids (player_id);

CREATE TABLE features_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players (id) ON DELETE CASCADE,
    as_of DATE NOT NULL,
    horizon_months INTEGER NOT NULL DEFAULT 6 CHECK (horizon_months = 6),
    payload JSONB NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (player_id, as_of, horizon_months)
);

CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players (id) ON DELETE CASCADE,
    as_of DATE NOT NULL,
    horizon_months INTEGER NOT NULL DEFAULT 6 CHECK (horizon_months = 6),
    delta_value_eur INTEGER NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('up', 'down', 'flat')),
    model_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX predictions_player_as_of_idx ON predictions (player_id, as_of DESC);
