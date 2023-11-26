import Header from "../../components/header";
import SubHeader from "../../components/subheader";
import OwingTiles from "./components/owing_tiles";
import DashboardTable from "./components/dashboard_table";
import './dashboard.css'


function Dashboard() {
  return (
    <>
      <div className="main">
        <Header text="Welcome back, Alex 👋" />
        <SubHeader text = "Here's your household expenses summary" />
        Household Balances
        <div className="container">
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
        </div>
        <div id="transaction_history_wrapper">
          Transaction History
        </div>

        <DashboardTable/>
      </div>
    </>
  );
}

export default Dashboard
