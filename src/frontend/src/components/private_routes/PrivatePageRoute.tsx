import React from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";

interface PrivateRouteProps {
  children: React.ReactNode;
}

const PrivatePageRoute = ({ children }: PrivateRouteProps) => {
  if (Cookies.get("household_id") == "null") {
    return <Navigate to="/Household/Setup" />;
  } else {
    return children;
  }
};

export default PrivatePageRoute;
