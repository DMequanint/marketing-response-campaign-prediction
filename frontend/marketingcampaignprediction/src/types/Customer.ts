// src/types/Customer.ts
export interface Customer {
  custAge: number;
  profession: string;
  marital: string;
  schooling: string;
  default: string;
  housing: string;
  contact: string;
  month: string;
  day_of_week: string;
  campaign: number;
  pdays: number;
  previous: number;
  poutcome: string;
  emp_var_rate: number;
  cons_price_idx: number;
  cons_conf_idx: number;
  euribor3m: number;
  nr_employed: number;
  pmonths: number;
  pastEmail: number;
}

export interface PredictionResponse {
  predictions: number[];
  probabilities: number[];
}

