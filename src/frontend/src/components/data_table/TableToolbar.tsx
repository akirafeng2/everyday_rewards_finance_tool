import { ReactNode } from "react";
import Delete from "../../assets/bin.svg";
import Filter from "../../assets/filter.svg";
import Export from "../../assets/export.svg";
import "./data_table.css";

interface TableToolbarProps {
  title: ReactNode;
  onDelete?: () => void;
  deleteDisabled?: boolean;
  actionLabel?: string;
  onAction?: () => void;
}

const TableToolbar = ({ title, onDelete, deleteDisabled, actionLabel, onAction }: TableToolbarProps) => {
  return (
    <div className="er_table_toolbar">
      <div className="er_table_toolbar_title">{title}</div>
      <div className="er_table_toolbar_actions">
        {onDelete && (
          <button type="button" className="er_toolbar_button" onClick={onDelete} disabled={deleteDisabled}>
            <img src={Delete} alt="" />
            Delete
          </button>
        )}
        <button type="button" className="er_toolbar_button">
          <img src={Filter} alt="" />
          Filters
        </button>
        <button type="button" className="er_toolbar_button outlined">
          <img src={Export} alt="" />
          Export
        </button>
        {actionLabel && (
          <button type="button" className="er_toolbar_button primary" onClick={onAction}>
            {actionLabel}
          </button>
        )}
      </div>
    </div>
  );
};

export default TableToolbar;
