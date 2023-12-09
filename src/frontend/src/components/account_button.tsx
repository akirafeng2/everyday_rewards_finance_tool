import "./account_button.css";
import chevron from "../assets/downChevron.png"

const AccountButton = () => {
  return (
    <div className="account_button">
      <div className="profile_circle" />
      <div className="vcontainer">
        <div className="name">Alex</div>
        <div className="account_type">User Account</div>
      </div>
      <img className="down_chevron" alt="down_chevron" src={chevron} />
    </div>
  );
};

export default AccountButton;
