// src/api/api.ts
import axios from "axios";
import { Customer } from "../types/Customer";

const API_BASE = "http://localhost:8000";

export const predictBatch = async (rows: Customer[]) => {
  const response = await axios.post(`${API_BASE}/predict`, rows);
  return response.data.predictions as number[];
};

