import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import RoleGuard from "./components/RoleGuard";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import HealthScore from "./pages/HealthScore";
import Chlorophyll from "./pages/Chlorophyll";
import DriftReports from "./pages/DriftReports";
import Alerts from "./pages/Alerts";
import NotAuthorized from "./pages/NotAuthorized";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />

        <Route path="/health" element={
          <ProtectedRoute><HealthScore /></ProtectedRoute>
        } />

        <Route path="/chlorophyll" element={
          <ProtectedRoute><Chlorophyll /></ProtectedRoute>
        } />

        <Route path="/drift" element={
          <ProtectedRoute><DriftReports /></ProtectedRoute>
        } />

        <Route path="/alerts" element={
          <RoleGuard allowedRoles={["government", "admin"]}>
            <Alerts />
          </RoleGuard>
        } />

        <Route path="/not-authorized" element={<NotAuthorized />} />
      </Routes>
    </BrowserRouter>
  );
}
