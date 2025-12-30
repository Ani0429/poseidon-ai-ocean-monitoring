import { useEffect, useState } from "react";
import "./OceanStatus.css";

const OceanStatus = () => {
  const [oceanData, setOceanData] = useState({
    temperature: 29.4,
    oxygen: 5.8,
    ph: 7.9,
    condition: "Moderate Stress"
  });

  // Simulate live digital twin updates
  useEffect(() => {
    const interval = setInterval(() => {
      setOceanData(prev => {
        const temp = +(prev.temperature + (Math.random() * 0.2 - 0.1)).toFixed(2);
        const oxygen = +(prev.oxygen + (Math.random() * 0.1 - 0.05)).toFixed(2);
        const ph = +(prev.ph + (Math.random() * 0.05 - 0.02)).toFixed(2);

        let condition = "Stable";
        if (temp > 29.5 || ph < 8.0) condition = "Moderate Stress";
        if (temp > 30 || ph < 7.8) condition = "High Stress";

        return { temperature: temp, oxygen, ph, condition };
      });
    }, 3000); // every 3 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="ocean-status-page">
      <h1>🌍 Global Ocean Status</h1>
      <p className="subtitle">
        Live digital twin view of ocean conditions derived from satellite & sensor data
      </p>

      <div className="status-grid">
        <div className="status-card">
          🌡 <h3>Sea Surface Temperature</h3>
          <p>{oceanData.temperature} °C</p>
        </div>

        <div className="status-card">
          💨 <h3>Dissolved Oxygen</h3>
          <p>{oceanData.oxygen} mg/L</p>
        </div>

        <div className="status-card">
          ⚗ <h3>Ocean pH</h3>
          <p>{oceanData.ph}</p>
        </div>

        <div className={`status-card highlight ${oceanData.condition.replace(" ", "").toLowerCase()}`}>
          ⚠ <h3>Overall Condition</h3>
          <p>{oceanData.condition}</p>
        </div>
      </div>
    </div>
  );
};

export default OceanStatus;
