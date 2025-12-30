import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export default function RoleGuard({ allowedRoles, children }) {
  const { user } = useContext(AuthContext);

  if (!user) return <Navigate to="/login" />;

  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/not-authorized" />;
  }

  return children;
}
