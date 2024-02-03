import React from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";

interface PrivateRouteProps {
  children: React.ReactNode;
}

const PrivatePageRoute = ({ children }: PrivateRouteProps) => {
  if (Cookies.get("user_id") == undefined) {
    return <Navigate to="/Login" />;
  } else if (Cookies.get("household_id") == undefined) {
    return <Navigate to="/Household" />;
  } else {
    return children;
  }
};

export default PrivatePageRoute;
