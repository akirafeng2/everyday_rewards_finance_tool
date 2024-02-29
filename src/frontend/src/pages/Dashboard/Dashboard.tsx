import Header from "../../components/headers/header";
import SubHeader from "../../components/headers/subheader";
import Tagline from "../../components/headers/tagline";
import OwingGroup from "./components/owing_group";
import DashboardTable from "./components/dashboard_table";
import Cookies from "js-cookie";
import "./dashboard.css";
import axios, { AxiosError, AxiosResponse } from "axios";
import { useState, useEffect } from "react";

function Dashboard() {
  function capitalizeFirstLetter(string: string | undefined) {
    if (typeof string == "string")
      return string.charAt(0).toUpperCase() + string.slice(1);
  }

  // Tagline: get date
  const [taglineText, setTaglineText] = useState<string>("Loading...");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5050/api/dashboard/get_earliest_date", {
        withCredentials: true,
      })
      .then((res: AxiosResponse) => {
        const earliestDate: string = res.data["date"];
        if (earliestDate == "") {
          setTaglineText("Your household is all settled up!");
        } else {
          setTaglineText(
            `Here's your household balances since the ${earliestDate}`
          );
        }
      })
      .catch((err: AxiosError) => {
        console.log(err);
        setTaglineText("Error fetching data");
      });
  }, []);

  return (
    <>
      <Header
        text={`Welcome back, ${capitalizeFirstLetter(
          Cookies.get("user_name")
        )} 👋`}
      />
      <Tagline text={taglineText} />
      <SubHeader text="Household Balances" />
      <OwingGroup />
      <SubHeader text="Unsettled Transactions" />
      <DashboardTable />
    </>
  );
}

export default Dashboard;
