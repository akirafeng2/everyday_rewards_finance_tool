import Header from "../../components/headers/header";
import SubHeader from "../../components/headers/subheader";
import OwingGroup from "./components/owing_group";
import DashboardTable from "./components/dashboard_table";
import UploadTile from "./components/upload_tiles";
import "./dashboard.css";

function Dashboard() {
  return (
    <div>
      <Header text="Welcome back, Alex 👋" />
      <SubHeader text="Here's your household expenses summary" />
      Household Balances
      <OwingGroup />
      <div className="hcontainer">
        <div className="vcontainer">
          <div id="transaction_history_wrapper">Transaction History</div>
          <DashboardTable />
        </div>
        <div className="vcontainer">
          <div id="upload_wrapper">Upload</div>
          <UploadTile colour="blue">Add one-off expense</UploadTile>
          <UploadTile colour="red">
            Upload everyday 
            <br/>
            rewards purchases
          </UploadTile>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
