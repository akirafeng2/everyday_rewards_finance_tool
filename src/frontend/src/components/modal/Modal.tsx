import { ReactNode } from "react";
import ReactModal from "react-modal";
import { ArrowBackIcon, CloseIcon } from "../icons/icons";
import "./modal.css";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onBack?: () => void;
  title: string;
  subtitle?: ReactNode;
  size?: "small" | "large";
  headerExtra?: ReactNode;
  footer?: ReactNode;
  children?: ReactNode;
}

const Modal = ({
  isOpen,
  onClose,
  onBack,
  title,
  subtitle,
  size = "small",
  headerExtra,
  footer,
  children,
}: ModalProps) => {
  return (
    <ReactModal
      isOpen={isOpen}
      onRequestClose={onClose}
      ariaHideApp={false}
      className={`er_modal ${size}`}
      overlayClassName="er_modal_overlay"
    >
      <div className="er_modal_topbar">
        {onBack ? (
          <button type="button" className="er_icon_button" aria-label="Back" onClick={onBack}>
            <ArrowBackIcon />
          </button>
        ) : (
          <span />
        )}
        <button type="button" className="er_icon_button" aria-label="Close" onClick={onClose}>
          <CloseIcon />
        </button>
      </div>
      <div className="er_modal_header">
        <div className="er_modal_title">{title}</div>
        {headerExtra}
      </div>
      {subtitle && <div className="er_modal_subtitle">{subtitle}</div>}
      <div className="er_modal_body">{children}</div>
      {footer && <div className="er_modal_footer">{footer}</div>}
    </ReactModal>
  );
};

export default Modal;
