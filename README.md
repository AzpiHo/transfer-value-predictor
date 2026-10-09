# Transfer value predictor

Monorepo scaffold for a football player transfer-value product. The prediction target is the **change in market value over six months**: a direction (`up`, `down`, or `flat`) and a magnitude in euros.

Scope is the Big 5 leagues — Premier League, La Liga, Serie A, Bundesliga, and Ligue 1 — plus the UEFA Champions League.

This repository is a shell. Ingest does not call the network. The API returns a deterministic mock. Training does not fit a model. Valuation labels are not loaded.

## Legal

Never scrape Transfermarkt. Never train on scraped Transfermarkt values. Do not add a Transfermarkt client, scraper, or scraping URL to this repo.

Market-value labels are future work. When they are added, they have to come from a source the project has a right to store and model: a commercially licensed valuation feed, a club or league data-sharing agreement, or another feed with those rights. See `packages/ml/README.md`.

Paid football data vendors (API-Football Pro, Sportmonks, and others) are optional and not assumed. The football client is selected with `FOOTBALL_API_PROVIDER`. The only adapter shipped here is `stub`.

## Architecture

```
football API stub ──┐
                    ├── ingest ──► feature store (Postgres) ──► offline training
ClubElo stub ───────┘              packages/features            packages/ml
                                                                     │
                                                                     ▼
                                                          prediction API (FastAPI)
                                                          services/api
                                                                     │
                                                                     ▼
                                                          dashboard (Next.js)
                                                          apps/web
```

1. **Ingest** (`packages/ingest`) reads provider-agnostic football data and free ClubElo ratings. Both are stubs. ClubElo's public CSV base is `http://api.clubelo.com/YYYY-MM-DD`; fetch is off unless `CLUBELO_FETCH_ENABLED=true`, and even then this build refuses to open a socket.
2. **Feature store** (`packages/features`) defines the player id schema and the Postgres tables: `players`, `player_external_ids`, `features_snapshot`, `predictions`. The in-memory store is for tests.
3. **Training** (`packages/ml`) plans four position-specific models (GK, DF, MF, FW) for the six-month Δ. `label_source` stays `unconfigured`.
4. **Prediction API** (`services/api`) serves `GET /health` and `GET /predictions/{player_id}`. OpenAPI is generated at `/openapi.json`.
5. **Dashboard** (`apps/web`) is a Next.js App Router shell: overview, player list, and a prediction detail page that calls the API when it is reachable.

Champions League is competition context, not a domestic league. Players are stored against a Big 5 league. UCL membership belongs in a later feature payload.

## Layout

```
apps/web                 Next.js dashboard
services/api             FastAPI prediction service
packages/ingest          Football API + ClubElo stubs
packages/features        Schema, feature-store interface, SQL migration
packages/ml              Offline training stub
```

Python packages use a `src/` layout and install as `ftv-features`, `ftv-ingest`, `ftv-ml`, and `ftv-api`. The Node workspace is pnpm and contains `apps/web` only.

## Local run

Requires Node 22, pnpm 10, and Python 3.11+.

```bash
cp .env.example .env

# Optional Postgres for the feature-store migration.
docker compose up -d postgres
psql "$DATABASE_URL" -f packages/features/migrations/001_init.sql

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-ci.txt
uvicorn ftv_api.main:app --reload --port "${API_PORT:-8000}"

pnpm install
pnpm dev:web
```

The dashboard listens on `WEB_PORT` (default 3000). The API listens on `API_PORT` (default 8000). Interactive API docs are at `http://localhost:8000/docs`.

The API stub and the dashboard do not need Postgres. The migration is there for the feature store when a driver is added.

## Environment

Copy `.env.example`. Do not commit `.env` or real keys.

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | Postgres URL. The compose file's local default is `postgresql://ftv:ftv@localhost:5432/ftv`. |
| `FOOTBALL_API_PROVIDER` | Football data adapter. Use `stub` (no network). Paid providers are not implemented. |
| `FOOTBALL_API_KEY` | Empty unless a future paid adapter is configured. |
| `CLUBELO_BASE_URL` | Free ClubElo CSV origin. Default `http://api.clubelo.com`. |
| `CLUBELO_FETCH_ENABLED` | `false` by default. `true` still does not fetch in this scaffold. |
| `API_PORT` | Prediction API port. Default `8000`. |
| `WEB_PORT` | Dashboard port. Default `3000`. |
| `WEB_ORIGIN` | Browser origin allowed to call the API. |
| `API_BASE_URL` | Base URL the dashboard server uses when it renders a prediction. Falls back to `NEXT_PUBLIC_API_BASE_URL`. |
| `NEXT_PUBLIC_API_BASE_URL` | Same API base, available to browser code if a later client calls it. |

## Tests

GitHub Actions installs the workspace and the Python packages without secrets.

- Web job: `pnpm typecheck` and `pnpm build`.
- Python job: `pytest` against the API (in-process), ingest stubs, schema, migration text, and the training plan.

```bash
pnpm typecheck
pnpm build
pip install -r requirements-ci.txt
pytest
```
