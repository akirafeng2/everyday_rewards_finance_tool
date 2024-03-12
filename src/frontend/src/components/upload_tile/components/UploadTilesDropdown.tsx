import React from "react";

interface UploadTileDropdownProps {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setManualModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadTileDropdown = ({ setIsOpen, setManualModalOpen }: UploadTileDropdownProps) => {
  
  const close_dropdown = () => {
    setIsOpen(false);
  };

  


  const manual_button_handle = () => {
    setManualModalOpen(true)
  }

  return (
    <div
      className="upload_tile_dropdown"
      onMouseLeave={close_dropdown}
    >
      <div className="uploadButton">Upload from Everyday Rewards</div>
      <div className="uploadButton" onClick={manual_button_handle}>Upload Manually</div>

    </div>
  );
};

export default UploadTileDropdown;
