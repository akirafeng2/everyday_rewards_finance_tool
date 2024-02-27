import { Link } from "react-router-dom";
import "./sidebar.css";

import Dashboard from "./buttons/dashboard-sidebar";
import Transactions from "./buttons/transactions-sidebar";
import Weights from "./buttons/weights-sidebar";
import Settings from "./buttons/settings-sidebar";
import Recurring from "./buttons/recurring-sidebar";
import Logout from "./buttons/logout-sidebar";
import { useState, ReactElement, useEffect } from "react";

import ToggleItems from "./utils/toggleItems";

function Sidebar({ activePage }: { activePage: string }) {
  // Data to identify which page for each link
  const sidebarItems = [
    "Dashboard",
    "Transactions",
    "Weights",
    "Recurring",
    "Settings",
    "Logout",
  ];
  
  const sidebarToggle = new ToggleItems(sidebarItems, activePage)

  const getFillOfIcon = (state: string) => {
    switch (state) {
      case "active":
        return "#FFFFFF";
      case "hover":
        return "#2095E5";
      default:
        return "#91A6BC";
    }
  };
  
  const [activeItem, setActiveItem] = useState(activePage)
  const [stateMap, setStateMap] = useState(sidebarToggle.getCurrentStates())
  const [hover, setHover] = useState("")

  const handleClick = (item: string) => {
    setActiveItem(item)
  }
  
  const handleHover = (item: string) => {
    if (item !== activeItem) {
      setHover(item !== hover ? item : "");
    }
  };
  
  useEffect(() => {
    setStateMap(sidebarToggle.getCurrentStates())
  }, [activeItem]);

  useEffect(() => {
    sidebarToggle.hoverItem(hover)
    setStateMap(sidebarToggle.getCurrentStates())
  }, [hover]);

  const iconComponentMap: { [key: string]: JSX.Element} = {
    "Dashboard": <Dashboard fill={getFillOfIcon(stateMap["Dashboard"])}></Dashboard>,
    "Transactions": <Transactions fill={getFillOfIcon(stateMap["Transactions"])}></Transactions>,
    "Weights": <Weights fill={getFillOfIcon(stateMap["Weights"])}></Weights>,
    "Recurring": <Recurring fill={getFillOfIcon(stateMap["Recurring"])}></Recurring>,
    "Settings": <Settings fill={getFillOfIcon(stateMap["Settings"])}></Settings>,
    "Logout": <Logout fill={getFillOfIcon(stateMap["Logout"])}></Logout>
  }


  const sidebarButtons = () => {
    let sidebarButtons: ReactElement[] = [];
  
    for (let i = 0; i < sidebarItems.length; i++) {
      const item = sidebarItems[i];
      
      sidebarButtons.push(
        <Link key={`sidebarItem-${item}`} to={`/${item}`}>
          <li className={stateMap[item]} onClick={() => handleClick(item)} onMouseEnter={() => handleHover(item)} onMouseLeave={() => handleHover(item)}>
            <span className="sidebar-icon">
              {iconComponentMap[item]}
            </span>
            {item}
          </li>
        </Link>
      );
    }
    
    return sidebarButtons;
  };

  return (
    <>
      <div className="Sidebar">
        <ul className="nav-menu-items">
          {sidebarButtons()}
        </ul>
      </div>
    </>
  );
}

export default Sidebar;
