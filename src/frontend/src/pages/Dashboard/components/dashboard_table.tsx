interface Transaction {
  t_id: string;
  item: string;
  date: string;
  payer: string;
  cost: string;
}

const DashboardTable = () => {
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
      cost: "1500.00",
    },
  ];
  return (
    <div className="dashboard_table_box">
      <table>
        <tr>
          <th className="item">Item Name</th>
          <th className="date">Transaction Date</th>
          <th className="payer">Who Paid?</th>
          <th className="cost">Cost</th>
        </tr>
        {mock_table.map((item) => (
          <tr key={item.t_id}>
            <td className="item">{item.item}</td>
            <td className="date">{item.date}</td>
            <td className="payer">{item.payer}</td>
            <td className="cost">{item.cost}</td>
          </tr>
        ))}
      </table>
    </div>
  );
};

export default DashboardTable;
