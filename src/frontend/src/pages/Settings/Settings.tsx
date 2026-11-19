import { useMemo, useState } from "react";
import Cookies from "js-cookie";
import Header from "../../components/headers/header";
import Tagline from "../../components/headers/tagline";
import SubHeader from "../../components/headers/subheader";
import { CopyIcon, ShareIcon } from "../../components/icons/icons";
import { getHouseholdMembers } from "../../utils/household";
import "../../components/data_table/data_table.css";
import "./settings.css";

function Settings() {
  const members = useMemo(getHouseholdMembers, []);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [copied, setCopied] = useState(false);
  const householdCode = Cookies.get("household_code");
  const householdName = Cookies.get("household_name") || "our household";

  const toggleSelected = (member: string) => {
    setSelected((previous) => {
      const next = new Set(previous);
      if (next.has(member)) next.delete(member);
      else next.add(member);
      return next;
    });
  };

  const copyCode = () => {
    if (!householdCode) return;
    navigator.clipboard?.writeText(householdCode).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const shareMailto = `mailto:?subject=${encodeURIComponent(
    `Join ${householdName} on Everyday Rewards Finance Tool`
  )}&body=${encodeURIComponent(`Use household code ${householdCode} to join ${householdName}.`)}`;

  return (
    <>
      <Header text="Settings" />
      <Tagline text="Manage your household and invite housemates" />

      <SubHeader text="Household admin" />
      <div className="er_table_box settings_section">
        <table className="er_table">
          <thead>
            <tr>
              <th className="center checkbox_col">Checkbox</th>
              <th>User</th>
              <th>Status</th>
              <th>Activity</th>
            </tr>
          </thead>
          <tbody>
            {members.map((member, i) => (
              <tr key={member}>
                <td className="center">
                  <input
                    type="checkbox"
                    aria-label={`Select ${member}`}
                    checked={selected.has(member)}
                    onChange={() => toggleSelected(member)}
                  />
                </td>
                <td>{member}</td>
                <td className="bold">{i === 0 ? "Admin" : "Member"}</td>
                <td className="muted">2 days ago</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <SubHeader text="Add Housemate" />
      <div className="add_housemate_card">
        {householdCode ? (
          <>
            <button type="button" className="household_code" onClick={copyCode} title="Copy household code">
              <CopyIcon />
              <span>{householdCode.split("").join(" ")}</span>
            </button>
            <a className="share_email" href={shareMailto}>
              <ShareIcon />
              {copied ? "Code copied!" : "Share via email"}
            </a>
          </>
        ) : (
          <div className="tagline household_code_missing">Log out and back in to see your household code.</div>
        )}
      </div>
    </>
  );
}

export default Settings;
