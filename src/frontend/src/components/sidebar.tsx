import {useLocation, Link} from 'react-router-dom'
import './sidebar.css'

import Dashboard from "./dashboard-sidebar";
import Transactions from "./transactions-sidebar";
import Weights from "./weights-sidebar";
import Settings from "./settings-sidebar";
import OneOff from "./oneOff-sidebar";

function Sidebar() {
    // Data to identify which page for each link
    const routeDataDashboard={
        current: 'Dashboard'
    }
    const routeDataTransactions={
        current: 'Transactions'
    }
    const routeDataWeights={
        current: 'Weights'
    }
    const routeOneOff={
        current: 'OneOff'
    }
    const routeDataSettings={
        current: 'Settings'
    }

    const location = useLocation();
    const state = location.state['current'];
    console.log(state);

    var dashboardClass='navbar-toggle'
    var transactionsClass='navbar-toggle'
    var oneOffClass='navbar-toggle'
    var weightsClass='navbar-toggle'
    var settingsClass='navbar-toggle'

    var dashboardColor="currentColor"
    var transactionsColor="currentColor"
    var oneOffColor="currentColor"
    var weightsColor="currentColor"
    var settingsColor="currentColor"

    if (state=="Weights"){
        weightsClass='navbar-toggle-active'
        weightsColor='#101934'
    }else if(state =="Transactions"){
        transactionsClass='navbar-toggle-active'
        transactionsColor='#101934'
    }else if(state=="Settings"){
        settingsClass='navbar-toggle-active'
        settingsColor='#101934'
    }else if (state=="OneOff"){
        oneOffClass='navbar-toggle-active'
        oneOffColor='#101934'
    }else{ // NOTE: since beginning will be null, all else is dashboard as we often start at dashboard
        dashboardClass='navbar-toggle-active'
        dashboardColor='#101934'
    }


  return (
    <>
        <div className="Sidebar">
            {/* <img src={Logo}/> */}
            <ul className='nav-menu-items'>
                <li className={dashboardClass}>
                    <span className="sidebar-icon">
                        <Dashboard fill={dashboardColor}/>
                    </span>
                    <Link to="/Dashboard" state = {routeDataDashboard}>Dashboard</Link>
                </li>
                <li className={transactionsClass}>
                    <span className="sidebar-icon">
                        <Transactions fill={transactionsColor}/>
                    </span>
                    <Link to="/Transactions" state ={routeDataTransactions}>Transactions</Link>
                </li>
                <li className={oneOffClass}>
                    <span className="sidebar-icon">
                        <OneOff fill={oneOffColor}/>
                    </span>
                    <Link to="/OneOff" state ={routeOneOff}>One-off costs</Link>
                </li>
                <li className={weightsClass}>
                    <span className="sidebar-icon">
                        <Weights fill={weightsColor}/>
                    </span>
                    <Link to="/Weights" state = {routeDataWeights}>Weights</Link>
                </li>
                <li className={settingsClass}>
                    <span className="sidebar-icon">
                        <Settings fill ={settingsColor}/>
                    </span>
                    <Link to="/Settings" state ={routeDataSettings}>Settings</Link>
                </li>
            </ul>
        </div>

    </>
  )
}

export default Sidebar
