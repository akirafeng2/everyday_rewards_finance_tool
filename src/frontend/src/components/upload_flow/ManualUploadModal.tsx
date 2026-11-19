import { useMemo, useState } from "react";
import Modal from "../modal/Modal";
import ItemEntryTable from "./ItemEntryTable";
import { EntryRow, emptyEntryRow } from "./entryRow";
import { CalendarIcon } from "../icons/icons";
import { getHouseholdMembers } from "../../utils/household";

interface ManualUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ManualUploadModal = ({ isOpen, onClose }: ManualUploadModalProps) => {
  const members = useMemo(getHouseholdMembers, []);
  const [rows, setRows] = useState<EntryRow[]>(() => [emptyEntryRow(members)]);
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));

  const close = () => {
    setRows([emptyEntryRow(members)]);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      size="large"
      title="Add New Items"
      headerExtra={
        <label className="er_pill date_pill">
          <CalendarIcon />
          <input type="date" aria-label="Purchase date" value={date} onChange={(e) => setDate(e.target.value)} />
        </label>
      }
      subtitle="Let’s add in a new item manually"
      footer={
        <>
          <button type="button" className="er_button secondary" onClick={close}>
            Cancel
          </button>
          <button type="button" className="er_button primary" onClick={close}>
            Save
          </button>
        </>
      }
    >
      <ItemEntryTable members={members} rows={rows} setRows={setRows} itemLabel="Item Name" payerLabel="Buyer" />
    </Modal>
  );
};

export default ManualUploadModal;
