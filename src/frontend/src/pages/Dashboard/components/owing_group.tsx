import OwingTile from "./owing_tile";

interface Owings {
  [name: string]: number;
}

const OwingGroup = () => {
  let mock_owings: Owings = {
    Alex: 1200,
    Steph: 400,
    Anna: -1600,
  };
  const names = Object.keys(mock_owings);
  return (
    <div className="hcontainer owings">
      {names.map((name) => (
        <OwingTile name={name} owes={mock_owings[name]}/>
      ))}
    </div>
  );
};

export default OwingGroup;
