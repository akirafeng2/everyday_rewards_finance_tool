import AccountButton from "../../components/account_button/account_button";
import { Outlet } from "react-router-dom"

function LayoutHousehold() {
    return (
    <>
    <AccountButton />
    <Outlet/>
    </>
    )
}

export default LayoutHousehold;