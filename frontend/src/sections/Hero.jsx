import "../styles/hero.css";

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-overlay">
        <div className="hero-card">
          <h1>Dive Into the Ocean</h1>

          <p className="hero-subtitle">
            AI-powered Ocean Health Monitoring System for Climate Action
          </p>

          <p className="hero-sdg">
            Supporting <strong>SDG 13</strong> (Climate Action) &{" "}
            <strong>SDG 14</strong> (Life Below Water)
          </p>

          <button className="hero-btn">
            Explore Research
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;
