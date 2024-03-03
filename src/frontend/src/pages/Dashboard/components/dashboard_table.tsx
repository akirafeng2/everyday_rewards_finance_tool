import { TransactionInterface } from "../Dashboard";

interface Transaction {
  t_id: string;
  item: string;
  date: string;
  payer: string;
  cost: string;
}

interface UnsettledTransactionsProps {
  unsettledTransactions: Array<TransactionInterface>
}

const DashboardTable = ({unsettledTransactions}: UnsettledTransactionsProps ) => {
  console.log(unsettledTransactions)
  const mock_table: Transaction[] = [
    {
      t_id: "1",
      item: "WW Sliced Frozen Strawberries 500g",
      date: "06 Jul 2023",
      payer: "Alex",
      cost: "6.20",
    },
    {
      t_id: "2",
      item: "Tomato",
      date: "12 Jul 2023",
      payer: "Steph",
      cost: "15000.00",
    },
  ];
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
              <td className="cost">{item.cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DashboardTable;
