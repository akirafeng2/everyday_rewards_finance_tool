import { useState } from "react";
import Cookies from "js-cookie";
import Header from "../../components/headers/header";
import Tagline from "../../components/headers/tagline";
import { getUserName } from "../../utils/household";
import "../../components/modal/modal.css";
import "./account.css";

function Account() {
  const [editing, setEditing] = useState(false);
  const [saved, setSaved] = useState({
    name: getUserName(),
    email: Cookies.get("user_email") || "alexander@gmail.com",
  });
  const [name, setName] = useState(saved.name);
  const [email, setEmail] = useState(saved.email);

  // user_name stays as the backend profile name; it is used for receipt folders
  const save = () => {
    Cookies.set("display_name", name);
    Cookies.set("user_email", email);
    setSaved({ name, email });
    setEditing(false);
  };

  const cancel = () => {
    setName(saved.name);
    setEmail(saved.email);
    setEditing(false);
  };

  return (
    <>
      <Header text="Edit Account" />
      <Tagline text="View and edit current account settings" />
      <div className="account_layout">
        <div className="account_avatar_column">
          <div className="account_avatar">{name.charAt(0)}</div>
          <button type="button" className="er_button secondary small">
            Edit avatar
          </button>
        </div>

        <div className="account_card">
          <div className="account_card_header">
            <span>Saved Information</span>
            {editing ? (
              <div className="account_card_actions">
                <button type="button" className="er_button secondary small" onClick={cancel}>
                  Cancel
                </button>
                <button type="button" className="er_button primary small" onClick={save}>
                  Save
                </button>
              </div>
            ) : (
              <button type="button" className="er_button secondary small" onClick={() => setEditing(true)}>
                Edit
              </button>
            )}
          </div>
          <div className="account_field">
            <span className="account_label">Your name</span>
            {editing ? (
              <input aria-label="Your name" value={name} onChange={(e) => setName(e.target.value)} />
            ) : (
              <span className="account_value">{name}</span>
            )}
          </div>
          <div className="account_field">
            <span className="account_label">Your email address</span>
            {editing ? (
              <input aria-label="Your email address" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            ) : (
              <span className="account_value">{email}</span>
            )}
          </div>
          <div className="account_field">
            <span className="account_label">Your password</span>
            <span className="account_value password">••••••••••••</span>
          </div>
        </div>

        <div className="account_status">
          <span className="account_label">Member Status</span>
          <span className="account_value">Admin</span>
        </div>
      </div>
    </>
  );
}

export default Account;
