# @ftv/web

Next.js App Router shell for the transfer-value dashboard.

- `/` — product scope and the pipeline
- `/players` — placeholder roster
- `/predictions/[playerId]` — direction and magnitude for the six-month horizon

The detail page calls `GET /predictions/{player_id}` on `NEXT_PUBLIC_API_BASE_URL` when that service is up, and otherwise shows the same mock rule locally. Figures are mocked either way.

```bash
pnpm dev
```
