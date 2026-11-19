import React from "react";

export type UploadMethod = "everyday_rewards" | "manual";

interface UploadTileDropdownProps {
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  onSelect: (method: UploadMethod) => void;
}

const UploadTileDropdown = ({ setIsOpen, onSelect }: UploadTileDropdownProps) => {
  const close_dropdown = () => {
    setIsOpen(false);
  };

  const select = (method: UploadMethod) => {
    setIsOpen(false);
    onSelect(method);
  };

  return (
    <div className="upload_tile_dropdown" onMouseLeave={close_dropdown}>
      <div className="uploadButton" onClick={() => select("everyday_rewards")}>
        Upload from Everyday Rewards
      </div>
      <div className="uploadButton" onClick={() => select("manual")}>
        Upload Manually
      </div>
    </div>
  );
};

export default UploadTileDropdown;
