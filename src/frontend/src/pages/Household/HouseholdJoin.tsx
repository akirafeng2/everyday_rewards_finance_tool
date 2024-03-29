import "./houeshold.css";
import React, { useState, useEffect } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";
import RedExclamation from "../Authentication/components/red_exclamation";
import HouseholdJoinModal from "./components/householdJoinModal";

const HouseholdJoin = () => {
  const [tileNumber, setTileNumber] = useState(0);
  const [householdCode, setHouseholdCode] = useState("");
  const [attempt, setAttempt] = useState("valid")
  const [modalOpen, setModalOpen] = useState(false)
  const [householdID, setHouseholdID] = useState("");
  const [householdName, setHouseholdName] = useState("");

  const findFocus = () => {
    setAttempt("valid")
    if (tileNumber == 8) {
      var selectedTile = document.getElementById("7") as HTMLInputElement;
      selectedTile.focus();
    } else {
      document.getElementById(tileNumber.toString())!.focus();
    }
  };

  const handleTileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let nativeEvent = e.nativeEvent as InputEvent;
    if (nativeEvent.inputType == "deleteContentBackward") {
      setHouseholdCode((previousState) => previousState.slice(0, -1));
    } else if (tileNumber < 8) {
      setTileNumber((previousState) => previousState + 1);
      setHouseholdCode((previousState) => previousState.concat(e.target.value));
    }
  };

  const handleBackspace = (e: React.KeyboardEvent<HTMLElement>) => {
    if (e.code == "Backspace" && tileNumber > 0) {
      setTileNumber((previousState) => previousState - 1);
    }
  };

  useEffect(() => {
    console.log(tileNumber)
    console.log(householdCode)
    findFocus();
  }, [tileNumber]);

  const selectText = () => {
    if (tileNumber == 8){
      var selectedTile = document.getElementById("7") as HTMLInputElement;
      selectedTile.setSelectionRange(1,1)
    }
  };
  const inputTiles = () => {
    let inputTiles = [];
    for (let i = 0; i < 8; i++) {
      inputTiles.push(
        <input
          className="inputTiles"
          key={i}
          type="text"
          id={i.toString()}
          maxLength={1}
          onFocus={findFocus}
          onInput={handleTileChange}
          onKeyDown={handleBackspace}
          onClick={selectText}
        ></input>
      );
    }
    return inputTiles;
  };

  const attemptJoinHousehold = (e: React.FormEvent) => {
    e.preventDefault();

    axios.post("http://127.0.0.1:5050/api/household/get_household_details", {
        household_code: householdCode,
      })
      .then((res: AxiosResponse) => {
        setHouseholdID(res.data['household_id'])
        setHouseholdName(res.data['household_name'])
        setModalOpen(previousState => !previousState);
      })
      .catch((err: AxiosError) => {
        console.log(err);
        setAttempt("invalid")
      });
  };

  return (
    <main className="household">
      <div className="title">Join a Household</div>
      <div className="whiteBox">
        <form className={attempt} onSubmit={attemptJoinHousehold}>
          <div className="subTitle">Add House Code</div>
          <div className="subText">
            Find the share code in household admin settings
          </div>
          {inputTiles()}
          <br />
          {
          attempt == "invalid" &&
          <div className="error">
          <RedExclamation></RedExclamation>
          <span className={attempt}>Sorry, we can't find your Household! </span>
          </div>
          }
          <div className="centrediv">
            <input
              type="submit"
              value="Confirm Code"
              className="button"
            ></input>
          </div>
        </form>
      </div>
      <HouseholdJoinModal 
        isOpen={modalOpen} 
        setIsOpen={setModalOpen}
        household_id={householdID} 
        household_name={householdName}
      ></HouseholdJoinModal>
    </main>
  );
};

export default HouseholdJoin;
