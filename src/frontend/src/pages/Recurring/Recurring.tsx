import { useMemo, useState } from "react";
import Header from "../../components/headers/header";
import Tagline from "../../components/headers/tagline";
import TableToolbar from "../../components/data_table/TableToolbar";
import { CalendarIcon } from "../../components/icons/icons";
import { getHouseholdMembers } from "../../utils/household";
import AddRecurringModal, { NewRecurringExpense } from "./components/AddRecurringModal";
import "../../components/data_table/data_table.css";
import "../../components/modal/modal.css";
import "./recurring.css";

interface RecurringExpense {
  id: string;
  itemName: string;
  payer: string;
  repeats: string;
  cost: string;
  nextPayment: string;
}

const buildSampleExpenses = (members: string[]): RecurringExpense[] => {
  const payer = (i: number) => members[i % members.length];
  return [
    { id: "1", itemName: "Rent", payer: payer(0), repeats: "Weekly", cost: "$1500", nextPayment: "15 Feb" },
    { id: "2", itemName: "Disney+", payer: payer(1), repeats: "Monthly", cost: "$20", nextPayment: "31 Feb" },
    { id: "3", itemName: "Netflix", payer: payer(0), repeats: "Monthly", cost: "$20", nextPayment: "15 Feb" },
    { id: "4", itemName: "Amazon Prime", payer: payer(2), repeats: "Monthly", cost: "$15", nextPayment: "31 Feb" },
    { id: "5", itemName: "Electricity and Water", payer: payer(1), repeats: "Monthly", cost: "$300", nextPayment: "31 Feb" },
    { id: "6", itemName: "Home and Contents Insurance", payer: payer(1), repeats: "Fortnightly", cost: "$250", nextPayment: "15 Feb" },
  ];
};

function Recurring() {
  const members = useMemo(getHouseholdMembers, []);
  const [expenses, setExpenses] = useState<RecurringExpense[]>(() => buildSampleExpenses(members));
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [modalOpen, setModalOpen] = useState(false);

  const toggleSelected = (id: string) => {
    setSelected((previous) => {
      const next = new Set(previous);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const deleteSelected = () => {
    setExpenses((previous) => previous.filter((e) => !selected.has(e.id)));
    setSelected(new Set());
  };

  const addExpenses = (newExpenses: NewRecurringExpense[], startDate: Date) => {
    const nextPayment = startDate.toLocaleDateString("en-AU", { day: "numeric", month: "short" });
    setExpenses((previous) => [
      ...previous,
      ...newExpenses.map((e, i) => ({
        id: `added-${Date.now()}-${i}`,
        itemName: e.itemName,
        payer: e.payer,
        repeats: e.repeats,
        cost: `$${e.cost}`,
        nextPayment,
      })),
    ]);
  };

  return (
    <>
      <Header text="Recurring Expenses" />
      <Tagline text="Here is a list of the household’s repeat expenses." />
      <TableToolbar
        title={
          <span className="er_pill">
            <CalendarIcon />
            01/01/2024 - Present
          </span>
        }
        onDelete={deleteSelected}
        deleteDisabled={selected.size === 0}
        actionLabel="+ Add recurring expense"
        onAction={() => setModalOpen(true)}
      />
      <div className="er_table_box recurring_table">
        <table className="er_table">
          <thead>
            <tr>
              <th className="center checkbox_col">Check</th>
              <th>Item Name</th>
              <th>Who Pays?</th>
              <th>Repeats</th>
              <th>Next Payment</th>
              <th className="right">Cost</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((expense) => (
              <tr key={expense.id}>
                <td className="center">
                  <input
                    type="checkbox"
                    aria-label={`Select ${expense.itemName}`}
                    checked={selected.has(expense.id)}
                    onChange={() => toggleSelected(expense.id)}
                  />
                </td>
                <td>{expense.itemName}</td>
                <td className="muted">{expense.payer}</td>
                <td className="bold">{expense.repeats}</td>
                <td className="muted">{expense.nextPayment}</td>
                <td className="bold right">{expense.cost}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <AddRecurringModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        members={members}
        onSave={addExpenses}
      />
    </>
  );
}

export default Recurring;
