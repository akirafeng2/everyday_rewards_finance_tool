import React from "react";
import ReactModal from "react-modal";
import axios, { AxiosError, AxiosResponse } from "axios";
import Cookies from "js-cookie";
import CalendarBubble from "../CalendarBubble/CalendarBubble";

import './ManualModal.css'

interface ManualModalProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const ManualModal = ({
  isOpen,
  setIsOpen,
}: ManualModalProps) => {
  
    const close_modal = () => {
    setIsOpen(false);
  };

//   const handleConfirm = () => {
//     axios
//       .post(

//       )
//       .then((res: AxiosResponse) => {

//       })
//       .catch((err: AxiosError) => {
//         console.log(err);
//       });
//   };

  return (
    <ReactModal className="manualModal" overlayClassName="manualModalOverlay" isOpen={isOpen} onRequestClose={close_modal} ariaHideApp={false}>
      <div className="titleSpace"></div>
      <div className="modalTitle">Add New Items</div> 
      <div className="modalSubTitle">Let's add in a new item manually</div> 
      <CalendarBubble>24 January 2024</CalendarBubble>
      <div className="manualModalTableBox">

      </div>
      <div className="manualModalButtonsBox">
        <button className="cancel">Cancel</button>
        <button className="save">Save</button>
      </div>
    </ReactModal>
  );
};

export default ManualModal;
