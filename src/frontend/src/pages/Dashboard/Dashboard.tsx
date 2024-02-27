import Header from "../../components/headers/header";
import SubHeader from "../../components/headers/subheader";
import Tagline from "../../components/headers/tagline";
import OwingGroup from "./components/owing_group";
import DashboardTable from "./components/dashboard_table";
import Cookies from "js-cookie";
import "./dashboard.css";

function Dashboard() {
  console.log(Cookies.get());
  return (
      <>
        <Header text="Welcome back, Alex 👋" />
        <Tagline text="Here's your household expenses summary" />
        <SubHeader text="Household Balances" />
        <OwingGroup />
        <SubHeader text="Transaction history" />
        <DashboardTable />
      </>
  );
}

export default Dashboard;
