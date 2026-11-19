import ChevronDown from "./assets/chevronDown";
import ChevronUp from "./assets/chevronUp";
import "./upload_tile.css";
import UploadTileDropdown, { UploadMethod } from "./components/UploadTilesDropdown";
import EverydayRewardsUploadModal from "../upload_flow/EverydayRewardsUploadModal";
import ManualUploadModal from "../upload_flow/ManualUploadModal";
import { useState } from "react";

const UploadTile = () => {
  const [uploadDropdownActive, setUploadDropdownActive] =
    useState<boolean>(false);
  const [mouseClickedY, setMouseClickedY] = useState<number>(0);
  const [activeModal, setActiveModal] = useState<UploadMethod | null>(null);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setUploadDropdownActive((previous) => !previous);
    setMouseClickedY(e.pageY);
  };

  const handleMouseLeaveButton = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (e.pageY < mouseClickedY && uploadDropdownActive) {
      setUploadDropdownActive((previous) => !previous);
    }
  };

  return (
    <div className="uploadDropdown">
      <button
        type="button"
        className="upload_tile"
        onClick={handleClick}
        onMouseLeave={handleMouseLeaveButton}
      >
        <div className="upload_spacer"></div>
        <div>Upload</div>
        {uploadDropdownActive ? <ChevronUp /> : <ChevronDown />}
      </button>
      {uploadDropdownActive ? (
        <UploadTileDropdown setIsOpen={setUploadDropdownActive} onSelect={setActiveModal} />
      ) : null}
      <EverydayRewardsUploadModal
        isOpen={activeModal === "everyday_rewards"}
        onClose={() => setActiveModal(null)}
      />
      <ManualUploadModal isOpen={activeModal === "manual"} onClose={() => setActiveModal(null)} />
    </div>
  );
};

export default UploadTile;
