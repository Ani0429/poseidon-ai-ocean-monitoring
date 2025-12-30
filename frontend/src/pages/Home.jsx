import "./Home.css";
import oceanVideo from "../assets/video/digital_twin_ocean.mp4";

export default function Home() {
  return (
    <div className="home-root">

      {/* FIXED BACKGROUND VIDEO */}
      <div className="video-layer">
        <video
          src={oceanVideo}
          autoPlay
          muted
          loop
          playsInline
        />
        <div className="video-overlay" />
      </div>

      {/* SCROLLING CONTENT */}
      <div className="content-layer">

        {/* HERO */}
        <section className="hero-section">
          <h1>POSEIDON</h1>
          <p className="subtitle">
            Digital Twin of the Global Ocean System
          </p>
          <span className="scroll-hint">Scroll down to dive ↓</span>
        </section>

        {/* SECTION 1 */}
        <section className="info-section left">
          <div className="info-box">
            <h2>Why Poseidon?</h2>
            <p>
              Earth’s oceans regulate climate, support marine life,
              and sustain billions of people.
            </p>
            <p>
              Climate change is disrupting these systems faster than
              traditional monitoring methods can track.
            </p>
          </div>
        </section>

        {/* SECTION 2 */}
        <section className="info-section right">
          <div className="info-box">
            <h2>What is a Digital Twin?</h2>
            <p>
              A digital twin is a virtual representation of a real-world system.
            </p>
            <p>
              Poseidon creates a visual and analytical twin of ocean processes
              using satellite and sensor data.
            </p>
          </div>
        </section>

        {/* SECTION 3 */}
        <section className="info-section left">
          <div className="info-box">
            <h2>Critical Ocean Issues Increasing Today</h2>
            <ul>
              <li><strong>Ocean Acidification</strong> — CO₂ absorption lowers pH.</li>
              <li><strong>Ocean Deoxygenation</strong> — Oxygen loss creates dead zones.</li>
              <li><strong>Rising Sea Temperatures</strong> — Heat stress damages reefs.</li>
              <li><strong>Coral Reef Degradation</strong> — Long-term ecosystem collapse.</li>
            </ul>
          </div>
        </section>

        {/* SECTION 4 */}
        <section className="info-section right">
          <div className="info-box">
            <h2>What Poseidon Detects</h2>
            <p>
              Poseidon applies AI models on processed satellite datasets
              to identify early warning signals.
            </p>
            <ul>
              <li>Coral bleaching risk</li>
              <li>Algal bloom formation</li>
              <li>Oxygen-depleted zones</li>
              <li>Marine heatwaves</li>
            </ul>
            <p className="note">
              Predictions are shown in dedicated analysis modules.
            </p>
          </div>
        </section>

        {/* SECTION 5 */}
        <section className="info-section left">
          <div className="info-box">
            <h2>Why Early Detection Matters</h2>
            <p>
              Most ocean damage becomes visible only after it is irreversible.
            </p>
            <p>
              Poseidon focuses on early indicators for preventive action.
            </p>
          </div>
        </section>

        {/* SPACER TO END VIDEO */}
        <div className="end-spacer" />

      </div>
    </div>
  );
}
