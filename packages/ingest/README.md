# ftv-ingest

Placeholders for the two free-first inputs:

- **Football API** — `FOOTBALL_API_PROVIDER` and `FOOTBALL_API_KEY`. The only adapter included is `stub`, which returns the Big 5 leagues plus the Champions League and performs no network I/O. Paid vendors are not assumed and are not called.
- **ClubElo** — free daily ratings. `CLUBELO_BASE_URL` defaults to `http://api.clubelo.com`. `CLUBELO_FETCH_ENABLED` defaults to false. While disabled, `fetch_ratings` returns an empty list. Enabling it raises `NotImplementedError` until an HTTP adapter exists, so CI never opens a socket.

Configuration is read from the environment by `IngestConfig.from_env`.
