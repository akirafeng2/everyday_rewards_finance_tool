import { useState } from "react";
import { Receipt } from "./sampleReceipts";
import "../data_table/data_table.css";
import "./upload_flow.css";

interface SplitCostsProps {
  receipt: Receipt;
  members: string[];
}

interface ItemSplit {
  weights: string[];
  saveWeights: boolean;
}

const SplitCosts = ({ receipt, members }: SplitCostsProps) => {
  const [splits, setSplits] = useState<Record<string, ItemSplit>>({});

  const splitFor = (itemId: string): ItemSplit =>
    splits[itemId] ?? { weights: members.map(() => ""), saveWeights: false };

  const update = (itemId: string, patch: Partial<ItemSplit>) =>
    setSplits((previous) => ({ ...previous, [itemId]: { ...splitFor(itemId), ...patch } }));

  return (
    <div className="entry_table_box">
      <table className="er_table entry_table">
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Cost</th>
            {members.map((member) => (
              <th key={member} className="center">
                {member}
              </th>
            ))}
            <th className="center">Save Weights?</th>
          </tr>
        </thead>
        <tbody>
          {receipt.items.map((item) => {
            const split = splitFor(item.id);
            return (
              <tr key={item.id}>
                <td>{item.itemName}</td>
                <td className="bold">{item.cost}</td>
                {members.map((member, i) => (
                  <td key={member} className="center">
                    <input
                      className="weight_input"
                      aria-label={`${member} weight for ${item.itemName}`}
                      type="number"
                      min={0}
                      placeholder="_"
                      value={split.weights[i]}
                      onChange={(e) =>
                        update(item.id, {
                          weights: split.weights.map((w, j) => (j === i ? e.target.value : w)),
                        })
                      }
                    />
                  </td>
                ))}
                <td className="center">
                  <input
                    type="checkbox"
                    aria-label={`Save weights for ${item.itemName}`}
                    checked={split.saveWeights}
                    onChange={(e) => update(item.id, { saveWeights: e.target.checked })}
                  />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default SplitCosts;
