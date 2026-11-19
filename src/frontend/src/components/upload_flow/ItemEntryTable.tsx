import { AddIcon, DeleteSmallIcon } from "../icons/icons";
import "../data_table/data_table.css";
import { EntryRow, emptyEntryRow } from "./entryRow";
import "./upload_flow.css";

interface ItemEntryTableProps {
  members: string[];
  rows: EntryRow[];
  setRows: (rows: EntryRow[]) => void;
  itemLabel: string;
  payerLabel: string;
  repeatOptions?: string[];
}

// Editable item grid shared by the manual upload and add recurring expense modals.
const ItemEntryTable = ({ members, rows, setRows, itemLabel, payerLabel, repeatOptions }: ItemEntryTableProps) => {
  const update = (id: string, patch: Partial<EntryRow>) =>
    setRows(rows.map((row) => (row.id === id ? { ...row, ...patch } : row)));

  const updateWeight = (row: EntryRow, index: number, value: string) =>
    update(row.id, { weights: row.weights.map((w, i) => (i === index ? value : w)) });

  return (
    <div className="entry_table_box">
      <table className="er_table entry_table">
        <thead>
          <tr>
            <th>{itemLabel}</th>
            <th>{payerLabel}</th>
            <th>Cost</th>
            {repeatOptions && <th>Repeat</th>}
            {members.map((member) => (
              <th key={member} className="center">
                {member}
              </th>
            ))}
            <th className="center">Delete?</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>
                <input
                  className="text_input"
                  aria-label={itemLabel}
                  placeholder="Example of an item here"
                  value={row.itemName}
                  onChange={(e) => update(row.id, { itemName: e.target.value })}
                />
              </td>
              <td>
                <select aria-label={payerLabel} value={row.payer} onChange={(e) => update(row.id, { payer: e.target.value })}>
                  {members.map((member) => (
                    <option key={member}>{member}</option>
                  ))}
                </select>
              </td>
              <td>
                <input
                  className="weight_input cost_input"
                  aria-label="Cost"
                  type="number"
                  min={0}
                  step={0.01}
                  placeholder="$"
                  value={row.cost}
                  onChange={(e) => update(row.id, { cost: e.target.value })}
                />
              </td>
              {repeatOptions && (
                <td>
                  <select aria-label="Repeat" value={row.repeats} onChange={(e) => update(row.id, { repeats: e.target.value })}>
                    {repeatOptions.map((option) => (
                      <option key={option}>{option}</option>
                    ))}
                  </select>
                </td>
              )}
              {members.map((member, i) => (
                <td key={member} className="center">
                  <input
                    className="weight_input"
                    aria-label={`${member} weight`}
                    type="number"
                    min={0}
                    placeholder="_"
                    value={row.weights[i]}
                    onChange={(e) => updateWeight(row, i, e.target.value)}
                  />
                </td>
              ))}
              <td className="center">
                <button
                  type="button"
                  className="er_icon_button"
                  aria-label="Delete row"
                  onClick={() => setRows(rows.filter((r) => r.id !== row.id))}
                >
                  <DeleteSmallIcon />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button type="button" className="add_another_item" onClick={() => setRows([...rows, emptyEntryRow(members)])}>
        Add another item?
        <AddIcon />
      </button>
    </div>
  );
};

export default ItemEntryTable;
