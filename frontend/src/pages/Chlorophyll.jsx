import { useState } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";
import "./Chlorophyll.css";

export default function Chlorophyll() {
  const [form, setForm] = useState({
    sst: "", ph: "", oxygen: "",
    nitrate: "", phosphate: "", silicate: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const predict = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chlorophyll/rf",
        Object.fromEntries(
          Object.entries(form).map(([k, v]) => [k, Number(v)])
        )
      );
      setResult(res.data);
    } catch {
      alert("Prediction failed");
    }
  };

  const features = Object.entries(form).map(([k, v]) => ({
    name: k.toUpperCase(),
    value: Number(v)
  }));

  return (
    <div className="chl-container">
      <h1>🌿 Algal Bloom AI</h1>

      <div className="chl-form">
        {Object.keys(form).map(k => (
          <input key={k} name={k} placeholder={k.toUpperCase()} onChange={handleChange} />
        ))}
        <button onClick={predict}>Predict Chlorophyll</button>
      </div>

      {result && (
        <div className="chl-result">
          <span className={`risk ${result.risk.toLowerCase()}`}>
            {result.risk} Risk
          </span>

          <p><b>Chlorophyll Class:</b> {result.chlorophyll_class}</p>
          <p><b>Model:</b> {result.model}</p>

          {/* Confidence */}
          <div className="confidence">
            <div
              className="confidence-fill"
              style={{ width: `${result.confidence * 100}%` }}
            >
              {Math.round(result.confidence * 100)}%
            </div>
          </div>

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={features}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#4fc3f7" />
            </BarChart>
          </ResponsiveContainer>

          {/* EXPLAINABLE AI */}
          <div className="explain-box">
            <h3>🧠 Why this prediction?</h3>
            <ul>
              <li>High nutrients (nitrate/phosphate) promote algal growth</li>
              <li>Low oxygen favors bloom persistence</li>
              <li>Warm SST accelerates chlorophyll production</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
