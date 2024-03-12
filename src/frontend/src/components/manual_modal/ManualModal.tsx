import React from "react";
import ReactModal from "react-modal";
import axios, { AxiosError, AxiosResponse } from "axios";
import Cookies from "js-cookie";

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
    <ReactModal className="manualModal" isOpen={isOpen} onRequestClose={close_modal} ariaHideApp={false}>

      {/* <input type="button" value="Save" onClick={handleConfirm}></input> */}
    </ReactModal>
  );
};

export default ManualModal;
