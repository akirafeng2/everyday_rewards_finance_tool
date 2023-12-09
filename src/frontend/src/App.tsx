import "./App.css";
import Header from "./components/header";
import SubHeader from "./components/subheader";
import OwingTiles from "./pages/Dashboard/components/owing_group";
import DashboardTable from "./pages/Dashboard/components/dashboard_table";

function App() {
  return (
    <>
      <div id="main">
        <Header text="Welcome back, Alex 👋" />
        <SubHeader text = "Here's your household expenses summary" />
        Household Balances
        <div className="container">
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
        </div>
        Transaction History
        <DashboardTable/>
      </div>
    </>
  );
}

export default App;
