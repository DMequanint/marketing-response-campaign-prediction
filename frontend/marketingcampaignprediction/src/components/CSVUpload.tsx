// src/components/CSVUpload.tsx
import React from "react";
import { parseCSV } from "../utils/csv";
import { Customer } from "../types/Customer";

interface Props {
  onDataLoaded: (rows: Customer[]) => void;
}

export const CSVUpload: React.FC<Props> = ({ onDataLoaded }) => {
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;

    const file = e.target.files[0];
    const data = await parseCSV(file);
    onDataLoaded(data);
  };

  return (
    <div>
      <h3>Upload Customer CSV</h3>
      <input type="file" accept=".csv" onChange={handleFileChange} />
    </div>
  );
};

