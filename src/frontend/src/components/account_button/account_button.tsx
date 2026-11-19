import { useState } from "react";
import { Link } from "react-router-dom";
import "./account_button.css";
import chevron from "./assets/downChevron.png";
import { getUserName } from "../../utils/household";

const AccountButton = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="account_button_wrapper" onMouseLeave={() => setOpen(false)}>
      <button type="button" className="account_button" onClick={() => setOpen((previous) => !previous)}>
        <div className="profile_circle" />
        <div className="vcontainer">
          <div className="name">{getUserName()}</div>
          <div className="account_type">User Account</div>
        </div>
        <img className={`down_chevron${open ? " open" : ""}`} alt="down_chevron" src={chevron} />
      </button>
      {open && (
        <div className="account_dropdown">
          <Link to="/Account" onClick={() => setOpen(false)}>
            Edit Account
          </Link>
          <Link to="/Settings" onClick={() => setOpen(false)}>
            Settings
          </Link>
          <Link to="/Logout" onClick={() => setOpen(false)}>
            Logout
          </Link>
        </div>
      )}
    </div>
  );
};

export default AccountButton;
