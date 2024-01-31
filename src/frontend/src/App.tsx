import "./App.css";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard.tsx";
import Transactions from "./pages/Transactions/Transactions";
import Weights from "./pages/Weights";
import Settings from "./pages/Settings";
import OneOff from "./pages/OneOff";
import PageLayout from "./pages/PageLayout.tsx";

import Login from "./pages/Authentication/login.tsx";
import Signup from "./pages/Authentication/signup.tsx";
import HouseholdSetup from "./pages/Authentication/HouseholdSetup.tsx";
import PrivatePageRoute from "./components/private_routes/PrivatePageRoute.tsx";
import PrivateHouseholdRoute from "./components/private_routes/PrivateHouseholdRoute.tsx";

// function App() {
//   return (
//     <>
//       <div id="main">
//         <Header text="Welcome back, Alex 👋" />
//         <SubHeader text = "Here's your household expenses summary" />
//         Household Balances
//         <div className="container">
//           <OwingTiles></OwingTiles>
//           <OwingTiles></OwingTiles>
//           <OwingTiles></OwingTiles>
//         </div>
//         Transaction History
//         <DashboardTable/>
//       </div>
//     </>
//   );
// }

function App() {
  return (
    <>
      <Routes>
        <Route path="/Login" element={<Login />} />
        <Route path="/Signup" element={<Signup />} />
        <Route path="/Household" element={<PrivateHouseholdRoute><HouseholdSetup /></PrivateHouseholdRoute>} />

        <Route path="/Page" element={<PrivatePageRoute><PageLayout /></PrivatePageRoute>}>
          <Route path="Dashboard" element={<Dashboard />} />
          <Route path="Transactions" element={<Transactions />} />
          <Route path="OneOff" element={<OneOff />} />
          <Route path="Weights" element={<Weights />} />
          <Route path="Settings" element={<Settings />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
