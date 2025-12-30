export default function OceanIssues() {
  return (
    <section
      style={{
        padding: "80px 10%",
        background: "#071c2f",
        color: "#ffffff"
      }}
    >
      <h2 style={{ fontSize: "32px", marginBottom: "30px" }}>
        Critical Ocean Issues Addressed by Poseidon
      </h2>

      <p style={{ maxWidth: "900px", marginBottom: "40px", opacity: 0.9 }}>
        Climate change is rapidly impacting ocean systems. Poseidon continuously
        monitors and predicts the following critical issues using AI and satellite data.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "30px" }}>
        <div>
          <h3>🧪 Ocean Acidification</h3>
          <p>
            Increased absorption of atmospheric CO₂ lowers ocean pH levels,
            weakening coral reefs and shell-based marine organisms.
          </p>
        </div>

        <div>
          <h3>🫧 Ocean Deoxygenation</h3>
          <p>
            Rising temperatures reduce dissolved oxygen levels, creating hypoxic
            zones that threaten fish and marine biodiversity.
          </p>
        </div>

        <div>
          <h3>🌡️ Rising Sea Surface Temperature</h3>
          <p>
            Sustained ocean warming disrupts ecosystems, alters species migration,
            and accelerates coral bleaching events.
          </p>
        </div>

        <div>
          <h3>🪸 Coral Reef Degradation</h3>
          <p>
            Combined stress from temperature rise and acidification leads to coral
            bleaching and long-term reef ecosystem collapse.
          </p>
        </div>
      </div>
    </section>
  );
}
