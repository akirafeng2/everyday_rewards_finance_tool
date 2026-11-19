import { useState } from "react";
import axios from "axios";
import Modal from "../../../components/modal/Modal";

interface SettleUpModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSettled: () => void;
}

const SettleUpModal = ({ isOpen, onClose, onSettled }: SettleUpModalProps) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const close = () => {
    setError(false);
    onClose();
  };

  const confirm = () => {
    setLoading(true);
    axios
      .post("http://127.0.0.1:5050/api/reset/month_reset", null, { withCredentials: true })
      .then(() => {
        onSettled();
        close();
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      title="Confirm Reset?"
      subtitle="Settling up will clear all household balances and unsettled transactions. This cannot be undone."
      footer={
        <>
          <button type="button" className="er_button secondary" onClick={close}>
            Cancel
          </button>
          <button type="button" className="er_button danger" disabled={loading} onClick={confirm}>
            {loading ? "Resetting..." : "Confirm Reset"}
          </button>
        </>
      }
    >
      {error && <div className="er_error_text">Something went wrong. Please try again.</div>}
    </Modal>
  );
};

export default SettleUpModal;
