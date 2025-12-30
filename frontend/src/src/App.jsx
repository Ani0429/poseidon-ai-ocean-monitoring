import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import HealthScore from "./pages/HealthScore";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/health" element={<HealthScore />} />
      </Routes>
    </Router>
  );
}

export default App;
