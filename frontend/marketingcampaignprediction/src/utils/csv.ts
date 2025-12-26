// src/utils/csv.ts
import Papa from "papaparse";
import { Customer } from "../types/Customer";

export const parseCSV = (file: File): Promise<Customer[]> => {
  return new Promise((resolve, reject) => {
    Papa.parse<Customer>(file, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      complete: (results) => resolve(results.data),
      error: (error) => reject(error),
    });
  });
};

