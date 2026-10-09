import { mockPrediction } from "@/lib/mock";
import type { Prediction } from "@/lib/types";

export async function loadPrediction(playerId: string): Promise<{
  prediction: Prediction;
  source: "api" | "local";
}> {
  const local = mockPrediction(playerId);
  const apiBase = (
    process.env.API_BASE_URL ||
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    ""
  ).replace(/\/$/, "");
  if (!apiBase) return { prediction: local, source: "local" };

  try {
    const response = await fetch(
      `${apiBase}/predictions/${encodeURIComponent(playerId)}`,
      { cache: "no-store" },
    );
    if (!response.ok) return { prediction: local, source: "local" };
    const body = (await response.json()) as Prediction;
    return { prediction: body, source: "api" };
  } catch {
    return { prediction: local, source: "local" };
  }
}
