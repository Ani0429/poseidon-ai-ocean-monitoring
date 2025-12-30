import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "../components/Navbar";

import Home from "./Home";
import HealthScore from "./HealthScore";
import CoralReef from "./CoralReef";
import Chlorophyll from "./Chlorophyll";
import SatelliteCNN from "./SatelliteCNN";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/health" element={<HealthScore />} />
        <Route path="/coral" element={<CoralReef />} />
        <Route path="/chlorophyll" element={<Chlorophyll />} />
        <Route path="/satellite" element={<SatelliteCNN />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
