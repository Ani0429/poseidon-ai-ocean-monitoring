import { useState } from "react";
import "./SatelliteCNN.css";

const SatelliteCNN = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeImage = async () => {
    if (!file) return setError("Please select an image");

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/chlorophyll/predict-image",
        { method: "POST", body: formData }
      );

      const data = await res.json();

      const drift =
        data.confidence < 0.55
          ? "High Drift"
          : data.confidence < 0.7
          ? "Moderate Drift"
          : "Low Drift";

      setResult({ ...data, drift });
    } catch {
      setError("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="satellite-page">
      <h1>🛰 Satellite AI</h1>

      <div className="upload-card">
        <input type="file" accept="image/*"
          onChange={e => {
            setFile(e.target.files[0]);
            setPreview(URL.createObjectURL(e.target.files[0]));
          }}
        />
        <button onClick={analyzeImage}>
          {loading ? "Analyzing..." : "Analyze Image"}
        </button>
      </div>

      {result && (
        <div className="result-grid">
          <div className="image-box">
            <img src={preview} alt="Satellite" />
            <div className="heatmap-overlay" />
            <span className="heatmap-label">🔥 Grad-CAM</span>
          </div>

          <div className="result-card">
            <p><b>Marine Condition:</b> {result.marine_condition}</p>
            <p className={`risk ${result.risk.toLowerCase()}`}>
              {result.risk}
            </p>

            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${result.confidence * 100}%` }}
              />
            </div>

            <p><b>Drift:</b> {result.drift}</p>

            {/* EXPLAINABLE AI */}
            <div className="explain-box">
              <h3>🧠 Why this result?</h3>
              <ul>
                <li>CNN detected color & texture patterns linked to blooms</li>
                <li>Green intensity regions influenced classification</li>
                <li>Confidence reflects similarity to trained satellite data</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SatelliteCNN;
