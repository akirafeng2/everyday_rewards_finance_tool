import axios, { AxiosError, AxiosResponse } from "axios";
import OwingTile from "./owing_tile";
import { useState, useEffect } from "react";

interface Owings {
  [name: string]: string;
}

const OwingGroup = () => {
  const [owings, setOwings] = useState<Owings>({});
  const [names, setNames] = useState<Array<string>>([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5050/api/dashboard/get_owings", {
        withCredentials: true,
      })
      .then((res: AxiosResponse) => {
        const owings_data: Owings = res.data;
        setOwings(owings_data);
        setNames(Object.keys(owings_data));
      })
      .catch((err: AxiosError) => {
        console.log(err);
      });
  }, []);
  return (
    <div className="hcontainer owings">
      {names.map((name) => (
        <OwingTile name={name} key={name} owes={owings[name]} />
      ))}
    </div>
  );
};

export default OwingGroup;
