import Chevron from "./assets/chevron";
import "./upload_tile.css"
import UploadTileModal from "./components/UploadTilesModal";
import { useState } from "react";

const UploadTile = () => {
  const [uploadModalActive, setUploadModalActive] = useState<boolean>(false)

  const handleClick = () => {
    setUploadModalActive(previous => !previous)
  }
  return (
    <>
    <div className="upload_tile" id="upload_tile_id" onClick={handleClick}>
      <div className="upload_spacer"></div>
      <div>Upload</div>
      <Chevron/>
    </div>
    <UploadTileModal isOpen = {uploadModalActive} setIsOpen={setUploadModalActive}></UploadTileModal>
    </>
  );
};

export default UploadTile;
