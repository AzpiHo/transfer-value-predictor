export type Direction = "up" | "down" | "flat";

export type Prediction = {
  player_id: string;
  horizon_months: number;
  direction: Direction;
  delta_value_eur: number;
  currency: string;
  model_version: string;
  scope: {
    leagues: string[];
    competitions: string[];
    horizon_months: number;
  };
  label_source: string;
  mocked: boolean;
};
