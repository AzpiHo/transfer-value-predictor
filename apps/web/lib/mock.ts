import { createHash } from "node:crypto";

import type { Direction, Prediction } from "@/lib/types";

const LEAGUES = ["EPL", "LA_LIGA", "SERIE_A", "BUNDESLIGA", "LIGUE_1"];

/**
 * Same digest rule as services/api/src/ftv_api/mock.py.
 * Node's crypto keeps this off the Web Crypto API, which browsers withhold
 * on non-HTTPS origins other than localhost.
 */
export function mockPrediction(playerId: string): Prediction {
  const digest = Number.parseInt(
    createHash("sha256").update(playerId).digest("hex").slice(0, 8),
    16,
  );
  const bucket = digest % 5;
  let direction: Direction = "down";
  let delta = -(((Math.floor(digest / 5) % 160) + 1) * 50_000);
  if (bucket === 0) {
    direction = "flat";
    delta = 0;
  } else if (bucket === 1 || bucket === 2) {
    direction = "up";
    delta = Math.abs(delta);
  }

  return {
    player_id: playerId,
    horizon_months: 6,
    direction,
    delta_value_eur: delta,
    currency: "EUR",
    model_version: "stub-0.1.0",
    scope: {
      leagues: LEAGUES,
      competitions: ["UCL"],
      horizon_months: 6,
    },
    label_source: "unconfigured",
    mocked: true,
  };
}
