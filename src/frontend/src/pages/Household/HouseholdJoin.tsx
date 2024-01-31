import "./houeshold.css";
import { Link } from "react-router-dom";
import Emoji from "./components/emoji";

const HouseholdJoin = () => {

  const inputTiles = () => {
    let inputTiles = []
    for (let i=0; i<8; i++) {
        inputTiles.push(<input className="inputTiles" type="text" key={i} maxLength={1}></input>)
    }
    return inputTiles;
  }

  return (
    <main className="household">
      <div className="title">Join a Household</div>
        <div className="whiteBox">

          <form>
          <div className="subTitle">Add House Code</div>
            <div className="subText">Find the share code in household admin settings</div>
            {inputTiles()}
        
          </form>
        </div>
    </main>
  );
};

export default HouseholdJoin;