import React, { useState } from "react";
import { Customer } from "../types/Customer";

interface CustomerFormProps {
  onSubmit: (customers: Customer[]) => void;
}

const numericFields: (keyof Customer)[] = [
  "custAge", "campaign", "pdays", "previous",
  "emp_var_rate", "cons_price_idx", "cons_conf_idx",
  "euribor3m", "nr_employed", "pmonths", "pastEmail"
];

const categoricalFields: (keyof Customer)[] = [
  "profession","marital","schooling","default",
  "housing","contact","month","day_of_week","poutcome"
];

// Example helper text from training data
const categoricalHints: Record<string, string[]> = {
  profession: ["admin", "blue-collar", "technician", "management", "services", "self-employed", "retired", "unemployed", "unknown"],
  marital: ["married", "single", "divorced", "unknown"],
  schooling: ["primary", "secondary", "high.school", "university.degree", "professional.course", "unknown"],
  default: ["yes", "no", "unknown"],
  housing: ["yes", "no", "unknown"],
  contact: ["cellular", "telephone", "unknown"],
  month: ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"],
  day_of_week: ["mon","tue","wed","thu","fri"],
  poutcome: ["unknown","failure","other","success"]
};

const CustomerForm: React.FC<CustomerFormProps> = ({ onSubmit }) => {
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
    poutcome: ""
  });

  const [predicting, setPredicting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCustomer(prev => ({
      ...prev,
      [name]: numericFields.includes(name as keyof Customer) ? Number(value) : value
    }));
  };

  const handlePredict = async () => {
    setPredicting(true);
    console.log("Submitting customer:", customer);
    await onSubmit([customer as Customer]);
    setPredicting(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 16 }}>
      <h2>Predict Customer Response</h2>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: 12
      }}>
        {numericFields.map(field => (
          <input
            key={field}
            type="number"
            name={field}
            value={customer[field] as number}
            onChange={handleChange}
            placeholder={field}
            style={{ width: "100%", padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
          />
        ))}

        {categoricalFields.map(field => (
          <div key={field} style={{ display: "flex", flexDirection: "column" }}>
            <input
              type="text"
              name={field}
              value={customer[field] as string}
              onChange={handleChange}
              placeholder={`${field} (e.g. ${categoricalHints[field].join(", ")})`}
              style={{ width: "100%", padding: 8, borderRadius: 4, border: "1px solid #ccc" }}
            />
            <small style={{ color: "#666", fontSize: 12 }}>
              Valid options: {categoricalHints[field].join(", ")}
            </small>
          </div>
        ))}
      </div>

      <button
        onClick={handlePredict}
        style={{
          marginTop: 16,
          padding: "10px 20px",
          borderRadius: 4,
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          cursor: predicting ? "not-allowed" : "pointer"
        }}
        disabled={predicting}
      >
        {predicting ? "Predicting..." : "Predict Single Customer"}
      </button>
    </div>
  );
};

export default CustomerForm;

