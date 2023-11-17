import "./App.css";
import Header from "./components/header";
import SubHeader from "./components/subheader";
import OwingTiles from "./components/owing_tiles";
import DashboardTable from "./components/dashboard_table";

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
