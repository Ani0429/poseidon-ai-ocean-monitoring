import { useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import "./HealthScore.css";

export default function HealthScore() {
  const [form, setForm] = useState({
    temperature: "",
    ph: "",
    oxygen: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/health/score",
        {
          temperature: Number(form.temperature),
          ph: Number(form.ph),
          oxygen: Number(form.oxygen)
        }
      );
      setResult(res.data);
    } catch {
      alert("Prediction failed. Check backend.");
    }
  };

  const chartData = result
    ? [
        { name: "Temperature", value: result.breakdown.temperature_score },
        { name: "pH", value: result.breakdown.ph_score },
        { name: "Oxygen", value: result.breakdown.oxygen_score }
      ]
    : [];

  return (
    <div className="health-container">
      <h1>🌍 Ocean Health Index</h1>
      <p className="subtitle">
        AI-based assessment of ocean condition using temperature, pH and oxygen.
      </p>

      <div className="health-card">
        <div className="inputs">
          <input name="temperature" placeholder="Temperature (°C)" onChange={handleChange} />
          <input name="ph" placeholder="pH" onChange={handleChange} />
          <input name="oxygen" placeholder="Oxygen (mg/L)" onChange={handleChange} />
          <button onClick={submit}>Analyze Health</button>
        </div>

        {result && (
          <div className="result">
            <span className={`badge ${result.risk.toLowerCase()}`}>
              {result.risk} Risk
            </span>

            <h2>Health Score: {result.health_score}/100</h2>

            <div className="chart-box">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={chartData}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#4fc3f7" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* EXPLAINABLE AI */}
            <div className="explain-box">
              <h3>🧠 Why this score?</h3>
              <ul>
                <li>
                  Temperature impact:{" "}
                  {form.temperature > 30
                    ? "High temperature reduces oxygen solubility"
                    : "Temperature is within safe range"}
                </li>
                <li>
                  pH impact:{" "}
                  {form.ph < 7.8
                    ? "Acidic conditions stress marine life"
                    : "pH is stable for marine ecosystems"}
                </li>
                <li>
                  Oxygen impact:{" "}
                  {form.oxygen < 4
                    ? "Low oxygen may cause dead zones"
                    : "Oxygen levels support healthy marine life"}
                </li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
