import Logo from '../assets/logo.png'
import {Link} from 'react-router-dom'
import './sidebar.css'


function Sidebar() {

  return (
    <>
        <div className="Sidebar">
            {/* <img src={Logo}/> */}
            <ul className='nav-menu-items'>
                <li className='navbar-toggle'>
                    <Link to="/Dashboard">Dashboard</Link>
                </li>
                <li className='navbar-toggle'>
                    <Link to="/Transactions">Transactions</Link>
                </li>
                <li className='navbar-toggle'>
                    <Link to="/Weights">Weights</Link>
                </li>
                <li className='navbar-toggle'>
                    <Link to="/Settings">Settings</Link>
                </li>
            </ul>
        </div>

    </>
  )
}

export default Sidebar
