import { useMemo, useRef, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import Modal from "../modal/Modal";
import SplitCosts from "./SplitCosts";
import { SAMPLE_RECEIPTS } from "./sampleReceipts";
import { CalendarIcon, InfoIcon } from "../icons/icons";
import { getHouseholdMembers } from "../../utils/household";
import "./upload_flow.css";

const SCRAPER_API = "http://127.0.0.1:5000/api/scrape_everyday_rewards";
const BACKEND_API = "http://127.0.0.1:5050/api";
const CODE_LENGTH = 6;

type Step = "login" | "mfa" | "uploaded" | "split" | "complete";

interface EverydayRewardsUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const EverydayRewardsUploadModal = ({ isOpen, onClose }: EverydayRewardsUploadModalProps) => {
  const members = useMemo(getHouseholdMembers, []);
  const [step, setStep] = useState<Step>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState<string[]>(Array(CODE_LENGTH).fill(""));
  const [error, setError] = useState(false);
  // receipts are downloaded but not yet saved to the database
  const [downloaded, setDownloaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [receiptIndex, setReceiptIndex] = useState(0);
  const codeRefs = useRef<Array<HTMLInputElement | null>>([]);

  const receipts = SAMPLE_RECEIPTS;

  const reset = () => {
    setStep("login");
    setEmail("");
    setPassword("");
    setCode(Array(CODE_LENGTH).fill(""));
    setError(false);
    setDownloaded(false);
    setLoading(false);
    setReceiptIndex(0);
  };

  const close = () => {
    reset();
    onClose();
  };

  const submitLogin = async () => {
    setLoading(true);
    setError(false);
    const household = Cookies.get("household_name") || "household";
    const name = Cookies.get("user_name") || "user";
    const form = new FormData();
    form.append("email", email);
    form.append("password", password);
    try {
      // Only receipts newer than the latest downloaded one (format 01Jan2024) are scraped
      const latest = await axios.get(`${BACKEND_API}/receipt/latest_receipt_date`, { withCredentials: true });
      await axios.post(
        `${SCRAPER_API}/${encodeURIComponent(household)}/${encodeURIComponent(name)}/${latest.data.latest_receipt_date}/entry`,
        form,
        { withCredentials: true }
      );
      setStep("mfa");
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const submitCode = async () => {
    setLoading(true);
    setError(false);
    const form = new FormData();
    form.append("SMS Code", code.join(""));
    try {
      if (!downloaded) {
        await axios.post(`${SCRAPER_API}/continue`, form, { withCredentials: true });
        setDownloaded(true);
      }
      await axios.post(`${BACKEND_API}/receipt/insert_receipts_to_db`, null, { withCredentials: true });
      setStep("uploaded");
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const updateCode = (index: number, value: string) => {
    const digit = value.replace(/\D/g, "").slice(-1);
    setCode((previous) => previous.map((c, i) => (i === index ? digit : c)));
    if (digit && index < CODE_LENGTH - 1) codeRefs.current[index + 1]?.focus();
  };

  const handleCodeKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !code[index] && index > 0) codeRefs.current[index - 1]?.focus();
  };

  const nextReceipt = () => {
    if (receiptIndex < receipts.length - 1) setReceiptIndex(receiptIndex + 1);
    else setStep("complete");
  };

  if (step === "login") {
    return (
      <Modal
        isOpen={isOpen}
        onClose={close}
        title="Login"
        subtitle="Let’s connect your Everyday Rewards account."
        footer={
          <>
            <button type="button" className="er_button secondary" onClick={close}>
              Cancel
            </button>
            <button
              type="button"
              className="er_button primary"
              disabled={!email || !password || loading}
              onClick={submitLogin}
            >
              {loading ? "Connecting..." : "Next"}
            </button>
          </>
        }
      >
        <label className="er_field">
          Email
          <input
            type="email"
            className={error ? "invalid" : ""}
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="er_field">
          Password
          <input
            type="password"
            className={error ? "invalid" : ""}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error && (
          <div className="er_error_text">
            <InfoIcon fill="#C80106" />
            Incorrect email or password. Please try again.
          </div>
        )}
      </Modal>
    );
  }

  if (step === "mfa") {
    return (
      <Modal
        isOpen={isOpen}
        onClose={close}
        onBack={() => setStep("login")}
        title="Enter 2FA code"
        subtitle="A code has been sent to you via SMS."
        footer={
          <>
            <button type="button" className="er_button secondary" onClick={close}>
              Cancel
            </button>
            <button
              type="button"
              className="er_button primary"
              disabled={code.some((c) => c === "") || loading}
              onClick={submitCode}
            >
              {loading ? "Uploading..." : downloaded ? "Retry" : "Next"}
            </button>
          </>
        }
      >
        <div className="mfa_code">
          {code.map((digit, i) => (
            <input
              key={i}
              ref={(el) => (codeRefs.current[i] = el)}
              className={error ? "invalid" : ""}
              aria-label={`Digit ${i + 1}`}
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => updateCode(i, e.target.value)}
              onKeyDown={(e) => handleCodeKeyDown(i, e)}
            />
          ))}
        </div>
        {error && (
          <div className="er_error_text mfa_error">
            <InfoIcon fill="#C80106" />
            {downloaded
              ? "Receipts were downloaded but couldn’t be saved. Please retry."
              : "Incorrect code. Please try again."}
          </div>
        )}
      </Modal>
    );
  }

  if (step === "uploaded") {
    return (
      <Modal
        isOpen={isOpen}
        onClose={close}
        title="Upload complete!"
        subtitle={
          <>
            Your most recent Everyday Rewards receipts have been imported. Next, let’s configure how
            each item should be split across the household.
          </>
        }
        footer={
          <button type="button" className="er_button primary" onClick={() => setStep("split")}>
            Next
          </button>
        }
      />
    );
  }

  if (step === "split") {
    const receipt = receipts[receiptIndex];
    return (
      <Modal
        isOpen={isOpen}
        onClose={close}
        onBack={receiptIndex > 0 ? () => setReceiptIndex(receiptIndex - 1) : undefined}
        size="large"
        title={`Receipt ${receiptIndex + 1} out of ${receipts.length}`}
        headerExtra={
          <span className="er_pill">
            <CalendarIcon />
            {receipt.date}
          </span>
        }
        subtitle="Let’s sort out who should chip in for each item."
        footer={
          <>
            <button type="button" className="er_button secondary" onClick={() => setStep("complete")}>
              Save and Close
            </button>
            <button type="button" className="er_button primary" onClick={nextReceipt}>
              {receiptIndex < receipts.length - 1 ? "Next Receipt" : "Finish"}
            </button>
          </>
        }
      >
        <SplitCosts key={receipt.id} receipt={receipt} members={members} />
      </Modal>
    );
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={close}
      title="Transactions complete!"
      subtitle="Perfect! All receipts and their splits have been saved. You can change the weightings of each item any time in the “Weights” section."
      footer={
        <button type="button" className="er_button primary" onClick={close}>
          Back to home
        </button>
      }
    />
  );
};

export default EverydayRewardsUploadModal;
