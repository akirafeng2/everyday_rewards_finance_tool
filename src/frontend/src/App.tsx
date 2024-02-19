import "./App.css";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard.tsx";
import Transactions from "./pages/Transactions/Transactions";
import Weights from "./pages/Weights";
import Settings from "./pages/Settings";
import OneOff from "./pages/OneOff";
import LayoutPage from "./pages/LayoutPage.tsx";

import Login from "./pages/Authentication/login.tsx";
import Signup from "./pages/Authentication/signup.tsx";
import HouseholdSetup from "./pages/Household/HouseholdSetup.tsx";
import PrivatePageRoute from "./components/private_routes/PrivatePageRoute.tsx";
import HouseholdJoin from "./pages/Household/HouseholdJoin.tsx";
import LayoutHousehold from "./pages/Household/LayoutHousehold.tsx";
import { BrowserRouter } from "react-router-dom";
import { SessionAuth } from "supertokens-auth-react/recipe/session";
// import SuperTokens from "supertokens-web-js";
// import Session from "supertokens-web-js/recipe/session";
// import EmailPassword from "supertokens-web-js/recipe/emailpassword";
import SuperTokens, { SuperTokensWrapper } from "supertokens-auth-react";
import Session from "supertokens-auth-react/recipe/session";
import EmailPassword from "supertokens-auth-react/recipe/emailpassword";

SuperTokens.init({
  appInfo: {
    appName: "erapp",
    apiDomain: "http://127.0.0.1:5050",
    websiteDomain: "http://127.0.0.1:5173",
    apiBasePath: "/api/auth",
    websiteBasePath: "/login",
  },
  recipeList: [Session.init(), EmailPassword.init()],
});

function App() {
  return (
    <>
      <SuperTokensWrapper>
        <BrowserRouter>
          <Routes>
            <Route path="/Login" element={<Login />} />
            <Route path="/Signup" element={<Signup />} />
            <Route
              path="/Household"
              element={
                <SessionAuth>
                  <LayoutHousehold />
                </SessionAuth>
              }
            >
              <Route path="Setup" element={<HouseholdSetup />} />
              <Route path="Join" element={<HouseholdJoin />} />
            </Route>
            <Route
              path="/Page"
              element={
                <SessionAuth>
                  <PrivatePageRoute>
                    <LayoutPage />
                  </PrivatePageRoute>
                </SessionAuth>
              }
            >
              <Route path="Dashboard" element={<Dashboard />} />
              <Route path="Transactions" element={<Transactions />} />
              <Route path="OneOff" element={<OneOff />} />
              <Route path="Weights" element={<Weights />} />
              <Route path="Settings" element={<Settings />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </SuperTokensWrapper>
    </>
  );
}

export default App;
