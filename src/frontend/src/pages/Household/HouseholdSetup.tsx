import "./houeshold.css";
import { Link } from "react-router-dom";
import Emoji from "./components/emoji";

const HouseholdSetup = () => {
  return (
    <main className="household">
      <div className="title">Set Up Your Household</div>
      <div className="householdOptions">
        <div className="whiteBox">
          <Emoji label="tools" symbol="🛠️" />
          <Link to="/household/create" className="householdButton">Create a <br/> Household </Link>
        </div>
        <div className="whiteBox">
          <Emoji label="house" symbol="🏠" />
          <Link to="/household/join" className="householdButton">Join a <br/> Household </Link>
        </div>
      </div>
    </main>
  );
};

export default HouseholdSetup;
