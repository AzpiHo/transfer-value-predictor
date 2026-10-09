import type { Metadata } from "next";
import Link from "next/link";

import { PredictionPanel } from "@/app/predictions/[playerId]/prediction-panel";
import { findSamplePlayer } from "@/lib/sample-players";

export const metadata: Metadata = {
  title: "Prediction",
};

export default async function PredictionPage({
  params,
}: {
  params: Promise<{ playerId: string }>;
}) {
  const { playerId } = await params;
  const player = findSamplePlayer(playerId);

  return (
    <>
      <p className="kicker">
        <Link href="/players">Players</Link>
        {" / "}
        six-month Δ
      </p>
      <h1>{player?.name ?? "Prediction"}</h1>
      <p className="lede">
        {player
          ? `${player.positionLabel} · ${player.leagueLabel} · ${player.club}`
          : "This id is not on the placeholder roster. The mock still returns a direction and a magnitude."}
      </p>
      <PredictionPanel playerId={playerId} />
    </>
  );
}
