// src/components/PredictionTable.tsx

import React from "react";
import { Customer } from "../types/Customer";

/**
 * Props for the PredictionTable component.
 *
 * data:
 *   Array of customer records that were sent for prediction.
 *
 * predictions:
 *   Binary class labels returned by the model (0 = no response, 1 = response).
 *
 * probabilities:
 *   Predicted probabilities for the positive class (response = 1).
 */
interface Props {
  data: Customer[];
  predictions: number[];
  probabilities: number[];
}

/**
 * PredictionTable
 *
 * Renders a tabular view of:
 * - Customer feature values
 * - Model predictions
 * - Prediction probabilities
 *
 * This component is typically used for:
 * - Batch predictions
 * - Auditing and inspecting model outputs
 *
 * The table dynamically adapts to the Customer schema,
 * making it resilient to future feature additions.
 */
export const PredictionTable: React.FC<Props> = ({
  data,
  predictions,
  probabilities,
}) => {
  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: 16,
      }}
    >
      <thead>
        <tr>
          {/* Dynamically render column headers based on Customer keys */}
          {Object.keys(data[0]).map((col) => (
            <th
              key={col}
              style={{
                border: "1px solid #ccc",
                padding: 6,
                backgroundColor: "#f5f6fa",
                fontWeight: 600,
              }}
            >
              {col}
            </th>
          ))}
          <th
            style={{
              border: "1px solid #ccc",
              padding: 6,
              backgroundColor: "#f5f6fa",
              fontWeight: 600,
            }}
          >
            Prediction
          </th>
          <th
            style={{
              border: "1px solid #ccc",
              padding: 6,
              backgroundColor: "#f5f6fa",
              fontWeight: 600,
            }}
          >
            Probability
          </th>
        </tr>
      </thead>

      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            {/* Render each feature value for the customer */}
            {Object.values(row).map((val, i) => (
              <td
                key={i}
                style={{
                  border: "1px solid #ccc",
                  padding: 6,
                  textAlign: "center",
                }}
              >
                {val}
              </td>
            ))}

            {/* Render model prediction */}
            <td
              style={{
                border: "1px solid #ccc",
                padding: 6,
                fontWeight: 500,
                textAlign: "center",
              }}
            >
              {predictions[idx]}
            </td>

            {/* Render predicted probability */}
            <td
              style={{
                border: "1px solid #ccc",
                padding: 6,
                textAlign: "center",
              }}
            >
              {(probabilities[idx] * 100).toFixed(2)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

