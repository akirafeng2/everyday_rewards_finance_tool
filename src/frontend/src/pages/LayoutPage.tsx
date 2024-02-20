import Sidebar from "../components/sidebartwo/sidebar"
import AccountButton from "../components/account_button/account_button"
import { Outlet } from "react-router-dom"

function LayoutPage() {
    return (
    <>
    <Sidebar />
    <AccountButton />
    <Outlet/>
    </>
    )
}

export default LayoutPage;