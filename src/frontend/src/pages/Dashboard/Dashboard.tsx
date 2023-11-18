import Header from "../../components/header";
import SubHeader from "../../components/subheader";
import OwingTiles from "./components/owing_tiles";
import DashboardTable from "./components/dashboard_table";
import UploadTile from "./components/upload_tiles";
import "./dashboard.css";

function Dashboard() {
  return (
    <>
      <div id="main">
        <Header text="Welcome back, Alex 👋" />
        <SubHeader text="Here's your household expenses summary" />
        Household Balances
        <div className="hcontainer">
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
          <OwingTiles></OwingTiles>
        </div>
        <div className="hcontainer">
          <div className="vcontainer">
            <div id="transaction_history_wrapper">Transaction History</div>
            <DashboardTable />
          </div>
          <div className="vcontainer">
            <div id="upload_wrapper">Upload</div>
            <UploadTile colour="red"/>
            <UploadTile colour="blue"/>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
