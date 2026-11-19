import { useMemo, useState } from "react";
import Header from "../../components/headers/header";
import Tagline from "../../components/headers/tagline";
import TableToolbar from "../../components/data_table/TableToolbar";
import TablePagination from "../../components/data_table/TablePagination";
import EverydayRewardsUploadModal from "../../components/upload_flow/EverydayRewardsUploadModal";
import { CalendarIcon } from "../../components/icons/icons";
import { getHouseholdMembers } from "../../utils/household";
import Down from "../../assets/down.svg";
import Up from "../../assets/up.svg";
import "../../components/data_table/data_table.css";
import "../../components/modal/modal.css";
import "./transactions.css";

interface Transaction {
  id: string;
  date: string;
  itemName: string;
  cost: string;
  paid: string;
}

const ROWS_PER_PAGE = 10;

// Placeholder until the transactions API is available.
const buildSampleTransactions = (members: string[]): Transaction[] =>
  Array.from({ length: 24 }, (_, i) => ({
    id: String(i + 1),
    date: `${10 + Math.floor(i / 6)} Dec 2023`,
    itemName: ["Butter", "Milk", "Eggs", "Bread", "Apples", "Coffee"][i % 6],
    cost: ["$4.00", "$2.00", "$6.20", "$3.50", "$5.10", "$12.00"][i % 6],
    paid: members[i % members.length],
  }));

function Transactions() {
  const members = useMemo(getHouseholdMembers, []);
  const [transactions, setTransactions] = useState<Transaction[]>(() => buildSampleTransactions(members));
  const [sortAscending, setSortAscending] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [page, setPage] = useState(1);
  const [uploadOpen, setUploadOpen] = useState(false);

  const sorted = useMemo(
    () => (sortAscending ? transactions : [...transactions].reverse()),
    [transactions, sortAscending]
  );
  const pageCount = Math.ceil(sorted.length / ROWS_PER_PAGE);
  const pageRows = sorted.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);
  const evenSplit = (1 / members.length).toFixed(2);

  const toggleSelected = (id: string) => {
    setSelected((previous) => {
      const next = new Set(previous);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const deleteSelected = () => {
    setTransactions((previous) => previous.filter((t) => !selected.has(t.id)));
    setSelected(new Set());
    setPage(1);
  };

  return (
    <>
      <Header text="Transaction History" />
      <Tagline text="View and manage all of your household’s imported transactions" />
      <TableToolbar
        title={
          <span className="er_pill">
            <CalendarIcon />
            {sorted.length > 0 ? `${transactions[0].date} - Present` : "No transactions"}
          </span>
        }
        onDelete={deleteSelected}
        deleteDisabled={selected.size === 0}
        actionLabel="+ Upload Everyday Rewards"
        onAction={() => setUploadOpen(true)}
      />
      <div className="er_table_box">
        <table className="er_table">
          <thead>
            <tr>
              <th className="center checkbox_col">Checkbox</th>
              <th>
                <button
                  type="button"
                  className="transactions_sort"
                  onClick={() => setSortAscending((previous) => !previous)}
                >
                  Transaction Date
                  <img src={sortAscending ? Up : Down} alt={sortAscending ? "Ascending" : "Descending"} />
                </button>
              </th>
              <th>Item Name</th>
              <th>Cost</th>
              <th>Who Paid?</th>
              {members.map((member, i) => (
                <th key={member} className={`center${i === 0 ? " weight_divider" : ""}`}>
                  {member}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageRows.map((transaction) => (
              <tr key={transaction.id}>
                <td className="center">
                  <input
                    type="checkbox"
                    aria-label={`Select ${transaction.itemName}`}
                    checked={selected.has(transaction.id)}
                    onChange={() => toggleSelected(transaction.id)}
                  />
                </td>
                <td className="muted">{transaction.date}</td>
                <td>{transaction.itemName}</td>
                <td className="bold">{transaction.cost}</td>
                <td>{transaction.paid}</td>
                {members.map((member, i) => (
                  <td key={member} className={`weight${i === 0 ? " weight_divider" : ""}`}>
                    {evenSplit}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <TablePagination page={page} pageCount={pageCount} setPage={setPage} />
      <EverydayRewardsUploadModal isOpen={uploadOpen} onClose={() => setUploadOpen(false)} />
    </>
  );
}

export default Transactions;
