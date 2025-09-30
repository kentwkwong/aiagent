import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContent";
import type { JSX } from "react";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/" replace />;

  return children;
};

export default ProtectedRoute;
