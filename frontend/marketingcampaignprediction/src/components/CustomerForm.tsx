// src/components/CustomerForm.tsx

import React, { useState } from "react";
import { Customer } from "../types/Customer";

/**
 * Shape of the prediction response returned by the backend.
 * - predictions: binary class labels (0 or 1)
 * - probabilities: predicted probabilities for the positive class
 */
interface PredictionResult {
  predictions: number[];
  probabilities: number[];
}

/**
 * Props for the CustomerForm component.
 * onSubmit:
 *   Callback provided by the parent (App.tsx) that sends
 *   one or more customers to the backend for prediction.
 */
interface CustomerFormProps {
  onSubmit: (customers: Customer[]) => void;
}

/**
 * Numeric features used by the model.
 * These are passed directly to LightGBM without scaling.
 */
const numericFields: (keyof Customer)[] = [
  "custAge",
  "campaign",
  "pdays",
  "previous",
  "emp_var_rate",
  "cons_price_idx",
  "cons_conf_idx",
  "euribor3m",
  "nr_employed",
  "pmonths",
  "pastEmail",
];

/**
 * Categorical features used by the model.
 * These rely on LightGBM's native categorical handling.
 */
const categoricalFields: (keyof Customer)[] = [
  "profession",
  "marital",
  "schooling",
  "default",
  "housing",
  "contact",
  "month",
  "day_of_week",
  "poutcome",
];

/**
 * Example categorical values derived from the training dataset.
 * These are used ONLY as UI hints and validation guidance.
 * The backend remains the source of truth.
 */
const categoricalHints: Record<string, string[]> = {
  profession: [
    "admin",
    "blue-collar",
    "technician",
    "management",
    "services",
    "self-employed",
    "retired",
    "unemployed",
    "unknown",
  ],
  marital: ["married", "single", "divorced", "unknown"],
  schooling: [
    "primary",
    "secondary",
    "high.school",
    "university.degree",
    "professional.course",
    "unknown",
  ],
  default: ["yes", "no", "unknown"],
  housing: ["yes", "no", "unknown"],
  contact: ["cellular", "telephone", "unknown"],
  month: [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
  ],
  day_of_week: ["mon", "tue", "wed", "thu", "fri"],
  poutcome: ["unknown", "failure", "other", "success"],
};

/**
 * CustomerForm
 *
 * Renders a form for single-customer prediction.
 * - Numeric fields are entered as numbers
 * - Categorical fields are entered as text with helper hints
 *
 * The form delegates prediction execution to the parent component.
 */
const CustomerForm: React.FC<CustomerFormProps> = ({ onSubmit }) => {
  /**
   * Local customer state.
   * Defaults are representative of typical values from the training data.
   */
  const [customer, setCustomer] = useState<Partial<Customer>>({
    custAge: 35,
    campaign: 1,
    pdays: -1,
    previous: 0,
    emp_var_rate: 1.1,
    cons_price_idx: 93.99,
    cons_conf_idx: -36.4,
    euribor3m: 4.857,
    nr_employed: 5191,
    pmonths: -1,
    pastEmail: 0,
    profession: "",
    marital: "",
    schooling: "",
    default: "",
    housing: "",
    contact: "",
    month: "",
    day_of_week: "",
    poutcome: "",
  });

  /** Indicates whether a prediction request is in progress */
  const [predicting, setPredicting] = useState(false);

  /** Stores the prediction result returned by the backend */
  const [result, setResult] = useState<PredictionResult | null>(null);

  /**
   * Handles input changes for both numeric and categorical fields.
   * Automatically casts numeric inputs to numbers.
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCustomer((prev) => ({
      ...prev,
      [name]: numericFields.includes(name as keyof Customer)
        ? Number(value)
        : value,
    }));
  };

  /**
   * Triggers prediction by passing the customer
   * data up to the parent component.
   */
  const handlePredict = async () => {
    setPredicting(true);
    setResult(null);
    try {
      await onSubmit([customer as Customer]);
    } finally {
      setPredicting(false);
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#f5f6fa",
        minHeight: "100vh",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          backgroundColor: "#fff",
          borderRadius: 10,
          boxShadow: "0 6px 20px rgba(0,0,0,0.1)",
          padding: 24,
          maxWidth: 900,
          margin: "0 auto",
        }}
      >
        <h2 style={{ color: "#333", marginBottom: 24 }}>
          Predict Customer Response
        </h2>

        {/* Input Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: 16,
          }}
        >
          {/* Numeric Inputs */}
          {numericFields.map((field) => (
            <div key={field}>
              <input
                type="number"
                name={field}
                value={customer[field] as number}
                onChange={handleChange}
                placeholder={field}
                style={{
                  width: "100%",
                  padding: 10,
                  borderRadius: 6,
                  border: "1px solid #ccc",
                  fontSize: 14,
                }}
              />
            </div>
          ))}

          {/* Categorical Inputs */}
          {categoricalFields.map((field) => (
            <div key={field}>
              <input
                type="text"
                name={field}
                value={customer[field] as string}
                onChange={handleChange}
                placeholder={`${field} (e.g. ${categoricalHints[field].join(
                  ", "
                )})`}
                style={{
                  width: "100%",
                  padding: 10,
                  borderRadius: 6,
                  border: "1px solid #ccc",
                  fontSize: 14,
                }}
              />
              <small style={{ color: "#666", fontSize: 12 }}>
                Options: {categoricalHints[field].join(", ")}
              </small>
            </div>
          ))}
        </div>

        {/* Submit Button */}
        <button
          onClick={handlePredict}
          disabled={predicting}
          style={{
            marginTop: 24,
            padding: "12px 28px",
            borderRadius: 6,
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            fontWeight: 500,
            cursor: predicting ? "not-allowed" : "pointer",
          }}
        >
          {predicting ? "Predicting..." : "Predict Single Customer"}
        </button>

        {/* Prediction Output */}
        {result && (
          <div
            style={{
              marginTop: 24,
              padding: 16,
              borderRadius: 6,
              backgroundColor: "#e6f7ff",
              color: "#0050b3",
            }}
          >
            <h3>Prediction Result</h3>
            <p>
              Predicted Class: {result.predictions[0]}
              <br />
              Probability: {(result.probabilities[0] * 100).toFixed(2)}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomerForm;

