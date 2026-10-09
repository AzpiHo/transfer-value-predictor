import { directionLabel, formatEur } from "@/lib/format";
import type { Prediction } from "@/lib/types";

export function PredictionPanel({
  prediction,
  source,
}: {
  prediction: Prediction;
  source: "api" | "local";
}) {
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
