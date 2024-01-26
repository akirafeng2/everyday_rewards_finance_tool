import "./authentication.css";
import { Link } from "react-router-dom";
import Emoji from "./components/emoji";

const HouseholdSetup = () => {
  return (
    <main className="auth">
      <div className="title">Set Up Your Household</div>
      <div className="householdOptions">
        <div className="whiteBox">
          <Emoji label="tools" symbol="🛠️"/>
        </div>
        <div className="whiteBox">
        <Emoji label="house" symbol="🏠"/>
        </div>
      </div>
    </main>
  );
};

export default HouseholdSetup;
