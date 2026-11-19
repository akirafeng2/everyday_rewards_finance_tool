import Sidebar from "../components/sidebar/sidebar";
import AccountButton from "../components/account_button/account_button";
import { useParams } from "react-router-dom";

import Dashboard from "./Dashboard/Dashboard.tsx";
import Transactions from "./Transactions/Transactions";
import Weights from "./Weights/Weights";
import Settings from "./Settings/Settings";
import Recurring from "./Recurring/Recurring";
import Account from "./Account/Account";
import Logout from "./Logout";
import OneOff from "./OneOff";
import "./../App.css";

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
      case "Recurring":
        return <Recurring />;
      case "Settings":
        return <Settings />;
      case "Account":
        return <Account />;
      case "Logout":
        return <Logout />;
      case "OneOff":
        return <OneOff />;
      default:
        return <div>Brotherman...</div>;
    }
  };

  return (
    <>
      <Sidebar activePage={pageToDisplay} />

      <div className="bufferMainContainer">
        <div className="sidebarBuffer" />
        <div className="main">
          <div className="content">
            <AccountButton />
            {renderPageComponent()}
          </div>
        </div>
      </div>
    </>
  );
}

export default LayoutPage;
