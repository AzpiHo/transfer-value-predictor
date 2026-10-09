export type SamplePlayer = {
  id: string;
  name: string;
  position: "GK" | "DF" | "MF" | "FW";
  positionLabel: string;
  league: string;
  leagueLabel: string;
  club: string;
};

export const SAMPLE_PLAYERS: SamplePlayer[] = [
  {
    id: "11111111-1111-4111-8111-111111111111",
    name: "Sample Keeper",
    position: "GK",
    positionLabel: "Goalkeeper",
    league: "EPL",
    leagueLabel: "Premier League",
    club: "Unassigned",
  },
  {
    id: "22222222-2222-4222-8222-222222222222",
    name: "Sample Fullback",
    position: "DF",
    positionLabel: "Defender",
    league: "LA_LIGA",
    leagueLabel: "La Liga",
    club: "Unassigned",
  },
  {
    id: "33333333-3333-4333-8333-333333333333",
    name: "Sample Midfielder",
    position: "MF",
    positionLabel: "Midfielder",
    league: "SERIE_A",
    leagueLabel: "Serie A",
    club: "Unassigned",
  },
  {
    id: "44444444-4444-4444-8444-444444444444",
    name: "Sample Forward",
    position: "FW",
    positionLabel: "Forward",
    league: "BUNDESLIGA",
    leagueLabel: "Bundesliga",
    club: "Unassigned",
  },
  {
    id: "55555555-5555-4555-8555-555555555555",
    name: "Sample Winger",
    position: "FW",
    positionLabel: "Forward",
    league: "LIGUE_1",
    leagueLabel: "Ligue 1",
    club: "Unassigned",
  },
];

export function findSamplePlayer(playerId: string): SamplePlayer | undefined {
  return SAMPLE_PLAYERS.find((player) => player.id === playerId);
}
