import { TransactionInterface } from "../Dashboard";

interface UnsettledTransactionsProps {
  unsettledTransactions: Array<TransactionInterface>;
}

const DashboardTable = ({
  unsettledTransactions,
}: UnsettledTransactionsProps) => {
  return (
    <div className="dashboard_table_box">
      <table>
        <thead>
          <tr>
            <th className="item">Item Name</th>
            <th className="date">Date</th>
            <th className="type">Source</th>
            <th className="payer">Who Paid?</th>
            <th className="cost">Cost</th>
          </tr>
        </thead>
        <tbody>
          {unsettledTransactions.map((item) => (
            <tr key={item.key}>
              <td className="item">{item.item_name}</td>
              <td className="date">{item.date}</td>
              <td className="type">{item.date}</td>
              <td className="payer">{item.payer}</td>
              <td className="cost">${item.cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DashboardTable;
