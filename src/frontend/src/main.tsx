import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import Sidebar from './components/sidebar.tsx'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from './pages/Dashboard'
import Transactions from './pages/Transactions'
import Weights from './pages/Weights'
import Settings from './pages/Settings'


import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>

    {/* Router defines what routes are available and which page it then checks out from that .
      Anything using these links should be placed inside BrowserRouter */}
    <BrowserRouter>
      <Sidebar />

      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/Dashboard" element={<Dashboard />} />
        <Route path="/Transactions" element={<Transactions />} />
        <Route path="/Weights" element={<Weights />} />
        <Route path="/Settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>

  </React.StrictMode>,
)
