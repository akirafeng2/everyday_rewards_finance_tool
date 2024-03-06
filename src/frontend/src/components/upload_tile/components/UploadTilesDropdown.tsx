import React from "react";

interface UploadTileDropdownProps {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadTileDropdown = ({ setIsOpen }: UploadTileDropdownProps) => {
  
  const close_dropdown = () => {
    setIsOpen(false);
  };

  return (
    <div
      className="upload_tile_dropdown"
      onMouseLeave={close_dropdown}
    >
      <div className="uploadButton">Upload from Everyday Rewards</div>
      <div className="uploadButton">Upload Manually</div>
    </div>
  );
};

export default UploadTileDropdown;
