import chevron from "../assets/chevron.png";
import { ReactNode } from "react";

interface UploadTileProps {
  children: ReactNode;
  colour: string;
}

const UploadTile = ({ children, colour }: UploadTileProps) => {
  return (
    <div className={"upload_tile " + colour}>
      <div className="hcontainer"></div>
      <div className="hcontainer upload_tile_text">
        {children}
        <img className="chevron" alt="chevron" src={chevron} />
      </div>
    </div>
  );
};

export default UploadTile;
