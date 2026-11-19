import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import { signOut } from "supertokens-auth-react/recipe/session";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    signOut().finally(() => {
      ["user_name", "user_email", "household_id", "household_name", "household_members"].forEach((cookie) =>
        Cookies.remove(cookie)
      );
      navigate("/Login");
    });
  }, [navigate]);

  return <div className="tagline">Logging out...</div>;
}

export default Logout;
