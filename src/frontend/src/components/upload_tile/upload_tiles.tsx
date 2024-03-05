import Chevron from "./assets/chevron";
import "./upload_tile.css"
import UploadTileDropdown from "./components/UploadTilesDropdown";
import { useState } from "react";

const UploadTile = () => {
  const [uploadDropdownActive, setUploadDropdownActive] = useState<boolean>(false)

  const handleClick = () => {
    setUploadDropdownActive(previous => !previous)
  }
  return (
    <div className="uploadDropdown">
    <button type="button" className="upload_tile" onClick={handleClick}>
      <div className="upload_spacer"></div>
      <div>Upload</div>
      <Chevron/>
    </button>
    {uploadDropdownActive ? <UploadTileDropdown setIsOpen={setUploadDropdownActive}/>: null}
    </div>
  );
};

export default UploadTile;
