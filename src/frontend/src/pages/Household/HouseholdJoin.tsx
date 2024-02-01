import "./houeshold.css";
import { useState, useEffect} from "react";
import { Link } from "react-router-dom";

const HouseholdJoin = () => {
  const [tileNumber, setTileNumber] = useState(0);
  const [householdCode, setHouseholdCode] = useState("");
  
  const findFocus = () => {
    if (tileNumber == 8) {
        document.getElementById("7")!.focus()
    }
    else {
        document.getElementById(tileNumber.toString())!.focus()
    }

  };

  const handleTileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let nativeEvent = e.nativeEvent
    if (nativeEvent.inputType == "deleteContentBackward") {
        setHouseholdCode(previousState => previousState.slice(0,-1))
        // Put in here logic to remove letter from end of the password
    }
    else if (tileNumber < 8) {
        setTileNumber(previousState => previousState + 1)
        setHouseholdCode(previousState => previousState.concat(e.target.value))
    }
  }

  const handleBackspace = (e: KeyboardEvent) => {
    if (e.code == "Backspace" && tileNumber > 0) {
        setTileNumber(previousState => previousState - 1)
    }
  }
  
  useEffect(() => {
        findFocus()
  }, [tileNumber])

  const inputTiles = () => {
    let inputTiles = [];
    for (let i = 0; i < 8; i++) {
      inputTiles.push(
        <input className="inputTiles" key={i} type="text" id={i.toString()} maxLength={1} onFocus={findFocus} onInput={handleTileChange} onKeyDown={handleBackspace}></input>
      );
    }
    return inputTiles;
  };

  return (
    <main className="household">
      <div className="title">Join a Household</div>
      <div className="whiteBox">
        <form>
          <div className="subTitle">Add House Code</div>
          <div className="subText">
            Find the share code in household admin settings
          </div>
          {inputTiles()}
          <br />
          <div className="centrediv">
            <input
              type="submit"
              value="Confirm Code"
              className="button"
            ></input>
          </div>
        </form>
      </div>
    </main>
  );
};

export default HouseholdJoin;
