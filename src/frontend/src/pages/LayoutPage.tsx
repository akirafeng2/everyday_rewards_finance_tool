import Sidebar from "../components/sidebar/sidebar";
import AccountButton from "../components/account_button/account_button";
import { useParams } from "react-router-dom";

import Dashboard from "./Dashboard/Dashboard.tsx";
import Transactions from "./Transactions/Transactions";
import Weights from "./Weights";
import Settings from "./Settings";
import OneOff from "./OneOff";

function LayoutPage() {
  const { Page } = useParams<{ Page: string }>();
  const pageToDisplay = Page || "Dashboard";

  const renderPageComponent = () => {
    switch (Page) {
      case "Dashboard":
        return <Dashboard />;
      case "Transactions":
        return <Transactions />;
      case "Weights":
        return <Weights />;
      case "Settings":
        return <Settings />;
      case "OneOff":
        return <OneOff />;
      default:
        return <div>Page not found</div>;
    }
  };

  return (
    <>
      <Sidebar activePage={pageToDisplay} />
      <AccountButton />
      {renderPageComponent()}
    </>
  );
}

export default LayoutPage;
