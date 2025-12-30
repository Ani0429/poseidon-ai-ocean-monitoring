import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  if (!user) return null;

  return (
    <nav style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "15px 30px",
      background: "linear-gradient(90deg, #001f3f, #003366)",
      color: "white"
    }}>
      <h3>🌊 Poseidon</h3>

      <div style={{ display: "flex", gap: "15px" }}>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/health">Health Score</Link>
        <Link to="/chlorophyll">Chlorophyll</Link>
        <Link to="/drift">Drift</Link>

        {(user.role === "government" || user.role === "admin") && (
          <Link to="/alerts">Alerts</Link>
        )}

        <button onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}
