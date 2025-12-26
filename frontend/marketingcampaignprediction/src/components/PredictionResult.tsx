// src/components/PredictionResult.tsx

import React from "react";
import { Customer } from "../types/Customer";

/**
 * Props for the PredictionResult component.
 *
 * customer:
 *   The customer record that was used for prediction.
 *   Included for traceability and potential future extensions
 *   (e.g. feature inspection, explanations).
 *
 * prediction:
 *   Binary class label predicted by the model.
 *   - 0: customer is unlikely to respond
 *   - 1: customer is likely to respond
 *
 * probability:
 *   Model confidence for the positive class (response = 1).
 */
interface Props {
  customer: Customer;
  prediction: number;
  probability: number;
}

/**
 * PredictionResult
 *
 * Displays the prediction outcome for a single customer.
 * This component is optimized for:
 * - Quick feedback during manual input
 * - Demonstrations and exploratory analysis
 *
 * For batch predictions, use PredictionTable instead.
 */
export const PredictionResult: React.FC<Props> = ({
  customer,
  prediction,
  probability,
}) => {
  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: 12,
        borderRadius: 6,
        backgroundColor: "#fafafa",
      }}
    >
      <h3>Prediction Result</h3>

      {/* Display model output */}
      <p>
        <strong>Predicted Class:</strong> {prediction}
        <br />
        <strong>Probability:</strong>{" "}
        {(probability * 100).toFixed(2)}%
      </p>
    </div>
  );
};

