import { useEffect, useState } from "react";
import { getHealthScore } from "../services/api";
import "../styles/sections.css";

export default function HealthScore() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHealthScore()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Health score error:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="page"><h2>Loading ocean health...</h2></div>;
  }

  if (!data) {
    return <div className="page"><h2>Unable to fetch health data</h2></div>;
  }

  const statusColor =
    data.status === "Healthy"
      ? "green"
      : data.status === "Warning"
      ? "orange"
      : "red";

  return (
    <div className="page">
      <h1>🌊 Ocean Health Score</h1>

      <div className="health-card">
        <h2 style={{ color: statusColor }}>
          {data.score} / 100
        </h2>

        <h3 style={{ color: statusColor }}>
          {data.status}
        </h3>

        <p className="explanation">
          {data.explanation}
        </p>
      </div>
    </div>
  );
}
