import type { Direction, Prediction } from "@/lib/types";

const LEAGUES = ["EPL", "LA_LIGA", "SERIE_A", "BUNDESLIGA", "LIGUE_1"];

async function sha256Prefix(playerId: string): Promise<number> {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(playerId),
  );
  const hex = [...new Uint8Array(digest)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
  return Number.parseInt(hex.slice(0, 8), 16);
}

export async function mockPrediction(playerId: string): Promise<Prediction> {
  const digest = await sha256Prefix(playerId);
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
