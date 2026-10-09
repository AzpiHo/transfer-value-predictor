import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Overview",
};

const STEPS = [
  {
    index: "01",
    title: "Ingest",
    body: "Football API provider stub, plus a ClubElo fetch that stays offline.",
  },
  {
    index: "02",
    title: "Features",
    body: "Player ids and a Postgres schema for snapshots. No driver yet.",
  },
  {
    index: "03",
    title: "Train",
    body: "Separate GK, DF, MF, and FW plans. Labels are unwired.",
  },
  {
    index: "04",
    title: "Predict",
    body: "FastAPI returns a mocked direction and euro magnitude.",
  },
  {
    index: "05",
    title: "Review",
    body: "This dashboard reads that payload when the API is running.",
  },
];

export default function HomePage() {
  return (
    <>
      <p className="kicker">Big 5 leagues + Champions League</p>
      <h1>Six-month change in market value.</h1>
      <p className="lede">
        Direction and magnitude of Δ value. The stack is free-first: a
        provider-agnostic football API stub and ClubElo ratings. Paid football
        APIs are optional later. Nothing here is a live valuation.
      </p>
      <ul className="chips">
        <li>Premier League</li>
        <li>La Liga</li>
        <li>Serie A</li>
        <li>Bundesliga</li>
        <li>Ligue 1</li>
        <li>Champions League</li>
        <li>Horizon: 6 months</li>
      </ul>
      <section className="pipeline" aria-label="Pipeline">
        {STEPS.map((step) => (
          <article className="step" key={step.index}>
            <small>{step.index}</small>
            <h2>{step.title}</h2>
            <p>{step.body}</p>
          </article>
        ))}
      </section>
    </>
  );
}
