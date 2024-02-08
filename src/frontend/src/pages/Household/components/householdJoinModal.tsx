import React from "react";
import ReactModal from "react-modal";
import axios, { AxiosError, AxiosResponse } from "axios";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

interface HouseholdJoinModalProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  household_id: string;
  household_name: string;
}

const HouseholdJoinModal = ({
  isOpen,
  setIsOpen,
  household_id,
  household_name,
}: HouseholdJoinModalProps) => {
  const close_modal = () => {
    setIsOpen(false);
  };
  const navigate = useNavigate();

  const handleConfirm = () => {
    axios
      .post("http://127.0.0.1:5050/api/household/join_household", {
        user_id: Cookies.get("user_id"),
        household_id: household_id,
      })
      .then((res: AxiosResponse) => {
        console.log(res);
        Cookies.set("household_id", household_id);
        Cookies.set("household_name", household_name);
        Cookies.set(
          "household_members",
          JSON.stringify(res.data["household_profile_list"])
        );
        navigate("/page/dashboard");
      })
      .catch((err: AxiosError) => {
        console.log(err);
      });
  };

  return (
    <ReactModal isOpen={isOpen} onRequestClose={close_modal}>
      <div>{household_id}</div>
      <div>{household_name}</div>
      <input type="button" value="Confirm" onClick={handleConfirm}></input>
    </ReactModal>
  );
};

export default HouseholdJoinModal;
