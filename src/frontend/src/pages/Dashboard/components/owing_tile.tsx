interface OwingTileProp {
  name: string;
  owes: string;
}

const OwingTile = ({ name, owes }: OwingTileProp) => {
  let owing_statement: string;

  if (owes == "0") {
    owing_statement = name + " is square";
  } else if (owes.charAt(0) == "-") {
    owing_statement = name + " is owed";
    owes = owes.substring(1);
  } else {
    owing_statement = name + " owes";
  }

  return (
    <div className="owings_box">
      <div className="hcontainer">
        <div className="profile_circle"></div>
        <div className="vcontainer">
          <div className="owing_text">{owing_statement}</div>
          <div className="owing_amount">${owes}</div>
        </div>
      </div>
    </div>
  );
};

export default OwingTile;
