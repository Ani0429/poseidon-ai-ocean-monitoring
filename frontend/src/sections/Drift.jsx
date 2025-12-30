import "../styles/sections.css";

export default function Drift() {
  return (
    <section className="section">
      <h2>Drift Reports</h2>
      <p>
        Poseidon continuously monitors data drift using Evidently AI to detect
        changes in ocean temperature, chlorophyll concentration, oxygen levels,
        and pH values.
      </p>
      <p>
        These reports ensure model reliability over time and help scientists
        trust predictions made under changing climate conditions.
      </p>
    </section>
  );
}
