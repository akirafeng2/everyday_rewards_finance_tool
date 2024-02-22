import { Link } from "react-router-dom";
import "./sidebar.css";

import Dashboard from "./buttons/dashboard-sidebar";
import Transactions from "./buttons/transactions-sidebar";
import Weights from "./buttons/weights-sidebar";
import Settings from "./buttons/settings-sidebar";
import OneOff from "./buttons/oneOff-sidebar";
import React, { useState, ReactElement, useEffect } from "react";

import ToggleItems from "./utils/toggleItems";

// Todo: Need to fix bug surrounding when mouse leaves the hover, too tired to think of solution right now

function Sidebar() {
  // Data to identify which page for each link
  const sidebarItems = [
    "Dashboard",
    "Transactions",
    "Weights",
    // "Recurring",
    "Settings",
    // "Logout",
  ];
  
  const sidebarToggle = new ToggleItems(sidebarItems)

  const getFillOfIcon = (state: string) => {
    if (state == "active") {
      return "#FFFFFF"
    }
    else if (state == "hover") {
      return "#2095E5"
    }
    else {
      return "#91A6BC"
    }
  } 

  const [activeItem, setActiveItem] = useState("Dashboard")
  const [stateMap, setStateMap] = useState(sidebarToggle.getCurrentStates())
  const [hover, setHover] = useState("")

  const handleClick = (item: string) => {
    setActiveItem(item)
  }
  
  const handleHover = (item: string) => {
    if (item != activeItem) {
      setHover(item)
    }
  }
  
  useEffect(() => {
    sidebarToggle.toggleItem(activeItem)
    setStateMap(sidebarToggle.getCurrentStates())
    console.log(stateMap)
  }, [activeItem]);

  useEffect(() => {
    sidebarToggle.hoverItem(hover)
    setStateMap(sidebarToggle.getCurrentStates())
    console.log(stateMap)
  }, [hover]);

  const iconComponentMap: { [key: string]: JSX.Element} = {
    "Dashboard": <Dashboard fill={getFillOfIcon(stateMap["Dashboard"])}></Dashboard>,
    "Transactions": <Transactions fill={getFillOfIcon(stateMap["Transactions"])}></Transactions>,
    "Weights": <Weights fill={getFillOfIcon(stateMap["Weights"])}></Weights>,
    // "Recurring": <Recurring fill={getFillOfIcon(sidebarToggle.getCurrentState("Recurring"))}></Recurring>,
    "Settings": <Settings fill={getFillOfIcon(stateMap["Settings"])}></Settings>,
    // "Logout": <Logout fill={getFillOfIcon(sidebarToggle.getCurrentState("Logout"))}></Logout>
  }


  const sidebarButtons = () => {
    let sidebarButtons: ReactElement[] = [];
    sidebarItems.forEach((item) => {
      sidebarButtons.push(
        <Link to={`/Page/${item}`}>
          <li className={stateMap[item]} onClick={() => handleClick(item)} onMouseEnter={() => handleHover(item)} onMouseLeave={() => handleHover(item)}>
            <span className="sidebar-icon">
              {iconComponentMap[item]}
            </span>
            {item}
          </li>
        </Link>
      );
    });
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
