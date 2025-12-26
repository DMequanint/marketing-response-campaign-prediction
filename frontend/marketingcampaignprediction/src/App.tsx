// src/App.tsx
import React, { useState } from "react";
import { Customer, PredictionResponse } from "./types/Customer";
import CustomerForm from "./components/CustomerForm";
import { PredictionResult } from "./components/PredictionResult";
import { PredictionTable } from "./components/PredictionTable";

const App: React.FC = () => {
  const [predictions, setPredictions] = useState<number[]>([]);
  const [probabilities, setProbabilities] = useState<number[]>([]);
  const [batchData, setBatchData] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);

  // ------------------------
  // Single customer prediction
  // ------------------------
  const handleSingleSubmit = async (customers: Customer[]) => {
    if (!customers || customers.length === 0) return;
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(customers), // Backend expects a list
      });

      const data: PredictionResponse = await response.json();

      if (data?.predictions && data?.probabilities) {
        setPredictions(data.predictions);
        setProbabilities(data.probabilities);
        setBatchData(customers);
      } else {
        console.error("Invalid backend response:", data);
        alert("Backend returned invalid prediction data");
      }
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Error fetching prediction from backend");
    } finally {
      setLoading(false);
    }
  };

  // ------------------------
  // Batch CSV prediction
  // ------------------------
  const handleBatchSubmit = async (customers: Customer[]) => {
    if (!customers || customers.length === 0) return;
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(customers),
      });

      const data: PredictionResponse = await response.json();

      if (data?.predictions && data?.probabilities) {
        setPredictions(data.predictions);
        setProbabilities(data.probabilities);
        setBatchData(customers);
      } else {
        console.error("Invalid backend response:", data);
        alert("Backend returned invalid batch prediction data");
      }
    } catch (err) {
      console.error("Batch prediction error:", err);
      alert("Error fetching batch predictions from backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Marketing Campaign Response Predictor</h1>

      {/* Form for single or batch submission */}
      <CustomerForm
        onSubmit={handleSingleSubmit}
        onSubmitBatch={handleBatchSubmit} // optional if batch is implemented
      />

      {/* Loading indicator */}
      {loading && <p>Loading predictions...</p>}

      {/* Display prediction results */}
      {!loading && predictions.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          {predictions.length === 1 ? (
            <PredictionResult
              customer={batchData[0]}
              prediction={predictions[0]}
              probability={probabilities[0]}
            />
          ) : (
            <PredictionTable
              data={batchData}
              predictions={predictions}
              probabilities={probabilities}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default App;

