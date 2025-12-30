import { useState } from "react";
import "./CoralReef.css";

export default function CoralReef() {
  const [form, setForm] = useState({
    temperature: "",
    ph: "",
    oxygen: ""
  });

  const [result, setResult] = useState(null);

  const assessCoralHealth = () => {
    const t = Number(form.temperature);
    const ph = Number(form.ph);
    const o = Number(form.oxygen);

    let status = "Healthy Reef";
    let alerts = [];
    let explanation = [];

    if (t > 30) {
      alerts.push("🔥 Coral Bleaching Risk Detected");
      explanation.push(
        "Sea surface temperature exceeds coral thermal tolerance, disrupting symbiotic algae."
      );
      status = "Bleaching Risk";
    }

    if (ph < 7.8) {
      alerts.push("⚠️ Ocean Acidification Stress");
      explanation.push(
        "Lower pH reduces calcium carbonate availability, weakening coral skeleton growth."
      );
      status = "Physiological Stress";
    }

    if (o < 4) {
      alerts.push("☠️ Hypoxia (Low Oxygen) Threat");
      explanation.push(
        "Reduced dissolved oxygen levels limit coral respiration and metabolic activity."
      );
      status = "Severe Ecological Stress";
    }

    setResult({
      status,
      alerts,
      explanation
    });
  };

  return (
    <div className="coral-container">
      {/* HEADER */}
      <div className="coral-header">
        <h1>🪸 Coral Reef Intelligence Module</h1>
        <p>
          AI-driven early warning system designed to detect coral reef stress,
          bleaching risk, and ecological collapse signals.
        </p>
      </div>

      {/* INPUT CARD */}
      <div className="coral-card">
        <h3 className="section-title">Environmental Conditions</h3>

        <div className="inputs">
          <input
            placeholder="Sea Surface Temperature (°C)"
            onChange={(e) => setForm({ ...form, temperature: e.target.value })}
          />
          <input
            placeholder="Ocean pH"
            onChange={(e) => setForm({ ...form, ph: e.target.value })}
          />
          <input
            placeholder="Dissolved Oxygen (mg/L)"
            onChange={(e) => setForm({ ...form, oxygen: e.target.value })}
          />

          <button onClick={assessCoralHealth}>
            Run Coral Risk Assessment
          </button>
        </div>

        {/* RESULTS */}
        {result && (
          <div className="result">
            <div className={`status ${result.status.toLowerCase().replace(/ /g, "-")}`}>
              {result.status}
            </div>

            <div className="alert-box">
              <h3>🚨 AI Disaster Alerts</h3>

              {result.alerts.length === 0 ? (
                <p className="safe">
                  No immediate coral degradation risks detected.
                </p>
              ) : (
                <ul>
                  {result.alerts.map((a, i) => (
                    <li key={i}>{a}</li>
                  ))}
                </ul>
              )}
            </div>

            <div className="explain-box">
              <h3>🧠 Explainability Layer</h3>
              <p className="explain-sub">
                Why Poseidon flagged this condition:
              </p>
              <ul>
                {result.explanation.map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
