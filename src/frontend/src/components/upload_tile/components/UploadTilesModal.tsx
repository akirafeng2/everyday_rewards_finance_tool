import React from "react";
import ReactModal from "react-modal";
import axios, { AxiosError, AxiosResponse } from "axios";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

interface UploadTileModalProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadTileModal = ({ isOpen, setIsOpen }: UploadTileModalProps) => {
  const close_modal = () => {
    setIsOpen(false);
  };

  return (
    <ReactModal
      className="upload_tile_modal"
      overlayClassName="upload_tile_overlay"
      isOpen={isOpen}
      onRequestClose={close_modal}
      parentSelector={() => document.getElementById("upload_tile_id")!}
    >
      <div className="uploadButton">Upload from Everyday Rewards</div>
      <div className="uploadButton">Upload Manually</div>
    </ReactModal>
  );
};

export default UploadTileModal;
