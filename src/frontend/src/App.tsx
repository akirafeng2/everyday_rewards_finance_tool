import "./App.css";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard/Dashboard.tsx";
import Transactions from "./pages/Transactions/Transactions";
import Weights from "./pages/Weights";
import Settings from "./pages/Settings";
import OneOff from "./pages/OneOff";
import Login from "./pages/Authentication/Login.tsx";
import PageLayout from "./pages/PageLayout.tsx";

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
          <Route path="/Login" element={<Login/>} />
          <Route path="/Page" element={<PageLayout />}>
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
