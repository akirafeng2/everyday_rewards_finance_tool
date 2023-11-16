import { useState } from 'react'
import {Link} from 'react-router-dom'
import './sidebar.css'

function Sidebar() {
  const [count, setCount] = useState(0)

  return (
    <>
        <div className="Sidebar">
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
