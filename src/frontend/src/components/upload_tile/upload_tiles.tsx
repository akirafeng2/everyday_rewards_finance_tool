import ChevronDown from "./assets/chevronDown";
import ChevronUp from "./assets/chevronUp";
import "./upload_tile.css"
import UploadTileDropdown from "./components/UploadTilesDropdown";
import { useState } from "react";

const UploadTile = () => {
  const [uploadDropdownActive, setUploadDropdownActive] = useState<boolean>(false)
  const [mouseClickedY, setMouseClickedY] = useState<number>(0)

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    setUploadDropdownActive(previous => !previous)
    setMouseClickedY(e.pageY)
  }

  const handleMouseLeaveButton = (e: React.MouseEvent<HTMLButtonElement>) => {
    if ((e.pageY < mouseClickedY) && (uploadDropdownActive)) {
      setUploadDropdownActive(previous => !previous)
    }
  }

  return (
    <div className="uploadDropdown">
    <button type="button" className="upload_tile" onClick={handleClick} onMouseLeave={handleMouseLeaveButton}>
      <div className="upload_spacer"></div>
      <div>Upload</div>
      {uploadDropdownActive ? <ChevronUp/> : <ChevronDown/>}
    </button>
    {uploadDropdownActive ? <UploadTileDropdown setIsOpen={setUploadDropdownActive}/>: null}
    </div>
  );
};

export default UploadTile;
