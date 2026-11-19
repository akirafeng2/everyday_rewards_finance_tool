import { useMemo, useState } from "react";
import Header from "../../components/headers/header";
import Tagline from "../../components/headers/tagline";
import TableToolbar from "../../components/data_table/TableToolbar";
import TablePagination from "../../components/data_table/TablePagination";
import { InfoIcon } from "../../components/icons/icons";
import { getHouseholdMembers } from "../../utils/household";
import "../../components/data_table/data_table.css";
import "../../components/modal/modal.css";
import "./weights.css";

export interface SavedWeighting {
  id: string;
  itemName: string;
  cost: string;
  // null until the household allocates a weight for that member
  weights: Array<number | null>;
}

const ROWS_PER_PAGE = 12;

const buildSampleWeightings = (memberCount: number): SavedWeighting[] => {
  const unallocated = Array.from({ length: 4 }, (_, i) => ({
    id: `new-${i}`,
    itemName: "Example of an item here",
    cost: "$75.67",
    weights: Array<number | null>(memberCount).fill(null),
  }));
  const allocated = Array.from({ length: 8 }, (_, i) => ({
    id: `saved-${i}`,
    itemName: "Example of an item here",
    cost: "$75.67",
    weights: Array<number | null>(memberCount).fill(0.33),
  }));
  return [...unallocated, ...allocated];
};

function Weights() {
  const members = useMemo(getHouseholdMembers, []);
  const [rows, setRows] = useState<SavedWeighting[]>(() => buildSampleWeightings(members.length));
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [page, setPage] = useState(1);

  const pageCount = Math.ceil(rows.length / ROWS_PER_PAGE);
  const pageRows = rows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);
  const unallocatedCount = rows.filter((row) => row.weights.some((w) => w === null)).length;

  const toggleSelected = (id: string) => {
    setSelected((previous) => {
      const next = new Set(previous);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const updateWeight = (rowId: string, memberIndex: number, value: string) => {
    const parsed = value === "" ? null : Number(value);
    setRows((previous) =>
      previous.map((row) =>
        row.id === rowId
          ? { ...row, weights: row.weights.map((w, i) => (i === memberIndex ? parsed : w)) }
          : row
      )
    );
  };

  const deleteSelected = () => {
    setRows((previous) => previous.filter((row) => !selected.has(row.id)));
    setSelected(new Set());
  };

  const addProduct = () => {
    setRows((previous) => [
      {
        id: `added-${Date.now()}`,
        itemName: "New product",
        cost: "$0.00",
        weights: Array<number | null>(members.length).fill(null),
      },
      ...previous,
    ]);
    setPage(1);
  };

  return (
    <>
      <Header text="Saved Weightings" />
      <Tagline text="View, adjust and edit saved weightings" />
      {unallocatedCount > 0 && (
        <div className="er_info_text weights_notice">
          <InfoIcon />
          There {unallocatedCount === 1 ? "is" : "are"} {unallocatedCount} new{" "}
          {unallocatedCount === 1 ? "item" : "items"} that need weights to be allocated!
        </div>
      )}
      <TableToolbar
        title={new Date().toLocaleDateString("en-AU", { month: "long", year: "numeric" })}
        onDelete={deleteSelected}
        deleteDisabled={selected.size === 0}
        actionLabel="+ Add Product"
        onAction={addProduct}
      />
      <div className="er_table_box">
        <table className="er_table">
          <thead>
            <tr>
              <th className="center checkbox_col">Checkbox</th>
              <th>Item Name</th>
              <th>Cost</th>
              {members.map((member, i) => (
                <th key={member} className={`center${i === 0 ? " weight_divider" : ""}`}>
                  {member}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageRows.map((row) => {
              const unallocated = row.weights.some((w) => w === null);
              return (
                <tr key={row.id} className={unallocated ? "highlight" : ""}>
                  <td className="center">
                    <input
                      type="checkbox"
                      aria-label={`Select ${row.itemName}`}
                      checked={selected.has(row.id)}
                      onChange={() => toggleSelected(row.id)}
                    />
                  </td>
                  <td>{row.itemName}</td>
                  <td className="bold">{row.cost}</td>
                  {row.weights.map((weight, i) => (
                    <td key={members[i]} className={`weight${i === 0 ? " weight_divider" : ""}`}>
                      <input
                        className="weight_input weights_page_input"
                        type="number"
                        min={0}
                        step={0.01}
                        placeholder="_"
                        aria-label={`${members[i]} weight for ${row.itemName}`}
                        value={weight ?? ""}
                        onChange={(e) => updateWeight(row.id, i, e.target.value)}
                      />
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <TablePagination page={page} pageCount={pageCount} setPage={setPage} />
    </>
  );
}

export default Weights;
