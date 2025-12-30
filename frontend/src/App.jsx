import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import HealthScore from "./pages/HealthScore";
import Chlorophyll from "./pages/Chlorophyll";
import SatelliteCNN from "./pages/SatelliteCNN";
import CoralReef from "./pages/CoralReef";

function App() {
  return (
    <Router>
      <Navbar />

      <div style={{ paddingTop: "80px" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/health" element={<HealthScore />} />
          <Route path="/coral" element={<CoralReef />} />
          <Route path="/chlorophyll" element={<Chlorophyll />} />
          <Route path="/satellite" element={<SatelliteCNN />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
