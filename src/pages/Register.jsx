import { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const API_URL = "https://poseidon-ai-ocean-monitoring.onrender.com";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(`${API_URL}/auth/register`, {
        email,
        password,
        role,
      });

      login(res.data.token);
      navigate("/");
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>🌍 Join Poseidon</h2>

      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        /><br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br /><br />

        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="student">🎓 Student</option>
          <option value="scientist">🔬 Scientist</option>
          <option value="government">🏛️ Government</option>
          <option value="ngo">🌱 NGO</option>
          <option value="admin">👑 Admin</option>
        </select><br /><br />

        <button type="submit">Create Account</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
