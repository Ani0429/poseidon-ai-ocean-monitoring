import { BrowserRouter, Routes, Route } from "react-router-dom";
import HealthScore from "./pages/HealthScore";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/health" element={<HealthScore />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
