import { useLocation, Link } from "react-router-dom";
import "./sidebar.css";

import Dashboard from "./buttons/dashboard-sidebar";
import Transactions from "./buttons/transactions-sidebar";
import Weights from "./buttons/weights-sidebar";
import Settings from "./buttons/settings-sidebar";
import OneOff from "./buttons/oneOff-sidebar";

function Sidebar() {
  // Data to identify which page for each link
  const routeDataDashboard = {
    current: "Dashboard",
  };
  const routeDataTransactions = {
    current: "Transactions",
  };
  const routeDataWeights = {
    current: "Weights",
  };
  const routeOneOff = {
    current: "OneOff",
  };
  const routeDataSettings = {
    current: "Settings",
  };

  var state = "Dashboard";
  const location = useLocation();
  if (location.state != null) {
    state = location.state["current"];
  }
  console.log(state);

  var dashboardClass = "navbar-toggle";
  var transactionsClass = "navbar-toggle";
  var oneOffClass = "navbar-toggle";
  var weightsClass = "navbar-toggle";
  var settingsClass = "navbar-toggle";

  var dashboardColor = "currentColor";
  var transactionsColor = "currentColor";
  var oneOffColor = "currentColor";
  var weightsColor = "currentColor";
  var settingsColor = "currentColor";

  if (state == "Weights") {
    weightsClass = "navbar-toggle-active";
    weightsColor = "#101934";
  } else if (state == "Transactions") {
    transactionsClass = "navbar-toggle-active";
    transactionsColor = "#101934";
  } else if (state == "Settings") {
    settingsClass = "navbar-toggle-active";
    settingsColor = "#101934";
  } else if (state == "OneOff") {
    oneOffClass = "navbar-toggle-active";
    oneOffColor = "#101934";
  } else {
    // NOTE: since beginning will be null, all else is dashboard as we often start at dashboard
    dashboardClass = "navbar-toggle-active";
    dashboardColor = "#101934";
  }

  return (
    <>
      <div className="Sidebar">
        {/* <img src={Logo}/> */}
        <ul className="nav-menu-items">
          <Link to="/Page/Dashboard" state={routeDataDashboard}>
            <li className={dashboardClass}>
              <span className="sidebar-icon">
                <Dashboard fill={dashboardColor} />
              </span>
              Dashboard
            </li>
          </Link>

          <Link to="/Page/Transactions" state={routeDataTransactions}>
            <li className={transactionsClass}>
              <span className="sidebar-icon">
                <Transactions fill={transactionsColor} />
              </span>
              Transactions
            </li>
          </Link>

          <Link to="/Page/OneOff" state={routeOneOff}>
            <li className={oneOffClass}>
              <span className="sidebar-icon">
                <OneOff fill={oneOffColor} />
              </span>
              One-off costs
            </li>
          </Link>

          <Link to="/Page/Weights" state={routeDataWeights}>
            <li className={weightsClass}>
              <span className="sidebar-icon">
                <Weights fill={weightsColor} />
              </span>
              Weights
            </li>
          </Link>

          <Link to="/Page/Settings" state={routeDataSettings}>
            <li className={settingsClass}>
              <span className="sidebar-icon">
                <Settings fill={settingsColor} />
              </span>
              Settings
            </li>
          </Link>
        </ul>
      </div>
    </>
  );
}

export default Sidebar;
