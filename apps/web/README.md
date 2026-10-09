# @ftv/web

Next.js App Router shell for the transfer-value dashboard.

- `/` — product scope and the pipeline
- `/players` — placeholder roster
- `/predictions/[playerId]` — direction and magnitude for the six-month horizon

The detail page asks the prediction API from the server (`API_BASE_URL`, or `NEXT_PUBLIC_API_BASE_URL`) and otherwise renders the same mock locally. Figures are mocked either way.

```bash
pnpm dev
```
