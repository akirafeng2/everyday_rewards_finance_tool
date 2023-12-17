import chevron from "../assets/chevron.png";
import clouds from "../assets/clouds_n_stuff.png"
import er_logo from "../assets/ER_logo.png"
import { ReactNode } from "react";

interface UploadTileProps {
  children: ReactNode;
  colour: string;
}

const UploadTile = ({ children, colour }: UploadTileProps) => {
  return (
    <div className={"upload_tile " + colour}>
      <div className="hcontainer">
        <img className="clouds" alt="clouds" src={clouds} />
        {colour === "red" &&
        <img className="er_logo" alt="er_logo" src={er_logo} />
        }
      </div>
      <div className="hcontainer upload_tile_text">
        {children}
        <img className="chevron" alt="chevron" src={chevron} />
      </div>
    </div>
  );
};

export default UploadTile;
