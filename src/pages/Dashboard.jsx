import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    axios
      .get("https://poseidon-ai-ocean-monitoring.onrender.com/")
      .then(() => setStatus("online"))
      .catch(() => setStatus("offline"));
  }, []);

  return (
    <div style={{ padding: "40px", color: "#003366" }}>
      <h1>🌊 Poseidon Dashboard</h1>

      <p style={{ maxWidth: "700px", marginTop: "10px" }}>
        Poseidon is an AI-powered ocean intelligence system that continuously
        monitors ocean health using satellite data and machine learning.
        It predicts risks such as acidification, oxygen loss, and ecosystem collapse.
      </p>

      <div style={{
        marginTop: "30px",
        padding: "15px",
        borderRadius: "10px",
        background: status === "online" ? "#e6fffa" : "#ffe6e6",
        width: "300px"
      }}>
        <strong>Backend Status:</strong>{" "}
        {status === "checking" && "⏳ Checking..."}
        {status === "online" && "🟢 Online"}
        {status === "offline" && "🔴 Offline"}
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: "20px",
        marginTop: "40px"
      }}>
        <FeatureCard title="📊 Ocean Health Score" desc="AI-based 0–100 ocean health index" />
        <FeatureCard title="🛰️ Chlorophyll Prediction" desc="CNN & RF satellite analysis" />
        <FeatureCard title="📈 Drift Monitoring" desc="Detects data & model drift" />
        <FeatureCard title="⚠️ Alerts" desc="Early warnings for ocean disasters" />
      </div>
    </div>
  );
}

function FeatureCard({ title, desc }) {
  return (
    <div style={{
      padding: "20px",
      borderRadius: "15px",
      background: "linear-gradient(145deg, #ffffff, #dfefff)",
      boxShadow: "5px 5px 15px rgba(0,0,0,0.1)"
    }}>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  );
}
