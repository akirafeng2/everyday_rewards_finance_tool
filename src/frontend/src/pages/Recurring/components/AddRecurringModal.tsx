import { useState } from "react";
import Modal from "../../../components/modal/Modal";
import ItemEntryTable from "../../../components/upload_flow/ItemEntryTable";
import { EntryRow, emptyEntryRow } from "../../../components/upload_flow/entryRow";
import { CalendarIcon } from "../../../components/icons/icons";
import { REPEAT_OPTIONS } from "../repeatOptions";

export interface NewRecurringExpense {
  itemName: string;
  payer: string;
  cost: string;
  repeats: string;
  weights: string[];
}

interface AddRecurringModalProps {
  isOpen: boolean;
  onClose: () => void;
  members: string[];
  onSave: (expenses: NewRecurringExpense[], startDate: Date) => void;
}

const AddRecurringModal = ({ isOpen, onClose, members, onSave }: AddRecurringModalProps) => {
  const [rows, setRows] = useState<EntryRow[]>(() => [emptyEntryRow(members)]);
  const [startDate, setStartDate] = useState(new Date().toISOString().slice(0, 10));

  const close = () => {
    setRows([emptyEntryRow(members)]);
    onClose();
  };

  const save = () => {
    const valid = rows.filter((row) => row.itemName.trim() !== "" && row.cost !== "");
    onSave(valid, new Date(startDate));
    close();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      size="large"
      title="Add Recurring Expense"
      headerExtra={
        <label className="er_pill date_pill">
          <CalendarIcon />
          <input type="date" aria-label="Start date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </label>
      }
      subtitle="Let’s add in a new recurring expense"
      footer={
        <>
          <button type="button" className="er_button secondary" onClick={close}>
            Cancel
          </button>
          <button type="button" className="er_button primary" onClick={save}>
            Save
          </button>
        </>
      }
    >
      <ItemEntryTable
        members={members}
        rows={rows}
        setRows={setRows}
        itemLabel="Expense"
        payerLabel="Payer?"
        repeatOptions={REPEAT_OPTIONS}
      />
    </Modal>
  );
};

export default AddRecurringModal;
