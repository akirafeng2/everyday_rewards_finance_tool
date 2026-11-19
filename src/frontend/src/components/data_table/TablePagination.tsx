import leftArrow from "../../assets/leftArrow.svg";
import rightArrow from "../../assets/rightArrow.svg";
import "./data_table.css";

interface TablePaginationProps {
  page: number;
  pageCount: number;
  setPage: (page: number) => void;
}

const TablePagination = ({ page, pageCount, setPage }: TablePaginationProps) => {
  const pages = Array.from({ length: Math.max(pageCount, 1) }, (_, i) => i + 1);
  return (
    <div className="er_table_pagination">
      <button type="button" aria-label="Previous page" onClick={() => setPage(Math.max(1, page - 1))}>
        <img src={leftArrow} alt="" />
      </button>
      {pages.map((p) => (
        <button
          type="button"
          key={p}
          className={p === page ? "active" : ""}
          onClick={() => setPage(p)}
        >
          {p}
        </button>
      ))}
      <button
        type="button"
        aria-label="Next page"
        onClick={() => setPage(Math.min(pages.length, page + 1))}
      >
        <img src={rightArrow} alt="" />
      </button>
    </div>
  );
};

export default TablePagination;
