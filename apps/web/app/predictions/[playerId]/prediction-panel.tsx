"use client";

import { useEffect, useState } from "react";

import { directionLabel, formatEur } from "@/lib/format";
import { mockPrediction } from "@/lib/mock";
import type { Prediction } from "@/lib/types";

type Source = "api" | "local";

export function PredictionPanel({ playerId }: { playerId: string }) {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [source, setSource] = useState<Source>("local");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ?? "";

    mockPrediction(playerId)
      .then((local) => {
        setPrediction((current) => current ?? local);
      })
      .catch(() => {
        setError("The local placeholder could not be built.");
      });

    if (!apiBase) return () => controller.abort();

    fetch(`${apiBase}/predictions/${encodeURIComponent(playerId)}`, {
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) throw new Error(`API responded ${response.status}`);
        return response.json() as Promise<Prediction>;
      })
      .then((body) => {
        setPrediction(body);
        setSource("api");
        setError(null);
      })
      .catch((caught: unknown) => {
        if (caught instanceof DOMException && caught.name === "AbortError") return;
        setSource("local");
      });

    return () => controller.abort();
  }, [playerId]);

  if (!prediction) {
    return (
      <section className="prediction" aria-busy="true">
        <article className="hero-card">
          <p className="kicker">Loading placeholder</p>
          <p className="figure">—</p>
          {error ? <p className="note">{error}</p> : null}
        </article>
      </section>
    );
  }

  return (
    <section className="prediction">
      <article className="hero-card">
        <p className="kicker">
          {source === "api" ? "Mocked API response" : "Local placeholder"}
        </p>
        <span className={`badge ${prediction.direction}`}>
          {directionLabel(prediction.direction)}
        </span>
        <p className="figure">{formatEur(prediction.delta_value_eur)}</p>
        <p className="note">
          {prediction.horizon_months}-month change in market value. Direction is{" "}
          {prediction.direction}; magnitude is the signed euro amount. Model{" "}
          {prediction.model_version}. Labels are {prediction.label_source}.
        </p>
      </article>
      <article className="meta-card">
        <dl>
          <dt>Player id</dt>
          <dd>{prediction.player_id}</dd>
          <dt>Horizon</dt>
          <dd>{prediction.horizon_months} months</dd>
          <dt>Leagues</dt>
          <dd>{prediction.scope.leagues.join(", ")}</dd>
          <dt>Competition</dt>
          <dd>{prediction.scope.competitions.join(", ")}</dd>
          <dt>Currency</dt>
          <dd>{prediction.currency}</dd>
        </dl>
      </article>
    </section>
  );
}
