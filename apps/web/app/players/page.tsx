import type { Metadata } from "next";
import Link from "next/link";

import { SAMPLE_PLAYERS } from "@/lib/sample-players";

export const metadata: Metadata = {
  title: "Players",
};

export default function PlayersPage() {
  return (
    <>
      <p className="kicker">Placeholder roster</p>
      <h1>Players</h1>
      <p className="lede">
        Fictional rows so the list and the prediction route have something to
        open. They are not a squad feed and they carry no market value.
      </p>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Player</th>
              <th>Position</th>
              <th>League</th>
              <th>Club</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_PLAYERS.map((player) => (
              <tr key={player.id}>
                <td>
                  <Link className="player-link" href={`/predictions/${player.id}`}>
                    {player.name}
                  </Link>
                </td>
                <td>{player.positionLabel}</td>
                <td>{player.leagueLabel}</td>
                <td>{player.club}</td>
                <td>
                  <Link className="ghost" href={`/predictions/${player.id}`}>
                    View Δ
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
