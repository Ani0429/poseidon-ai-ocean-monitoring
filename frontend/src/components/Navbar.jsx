import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      {/* LEFT: LOGO */}
      <div className="navbar-logo">
        🌊 <span>POSEIDON</span>
      </div>

      {/* RIGHT: LINKS */}
      <ul className="navbar-links">
        <li>
          <Link to="/">🌊 Ocean Overview</Link>
        </li>
        <li>
          <Link to="/health">🧭 Ocean Health Index</Link>
        </li>
        <li>
          <Link to="/coral">🪸 Coral Reefs</Link>
        </li>
        <li>
          <Link to="/chlorophyll">🛰️ Algal Bloom AI</Link>
        </li>
        <li>
          <Link to="/satellite">🧠 Satellite AI</Link>
        </li>
      </ul>
    </nav>
  );
}
