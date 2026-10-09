# ftv-api

Prediction API stub.

- `GET /health` — liveness, no database.
- `GET /predictions/{player_id}` — mocked 6-month Δ market value: `direction` (`up`, `down`, `flat`) and `delta_value_eur` (signed magnitude; flat is `0`).
- `GET /openapi.json` and `GET /docs` — generated OpenAPI.

Any player id matching `^[A-Za-z0-9-]{1,64}$` returns a deterministic mock. The handler does not read Postgres and does not call a football API.

```bash
uvicorn ftv_api.main:app --reload --port "${API_PORT:-8000}"
```
