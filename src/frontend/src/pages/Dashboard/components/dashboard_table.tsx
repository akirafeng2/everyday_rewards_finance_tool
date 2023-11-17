const DashboardTable = () => {
  return (
    <div className="dashboard_table_box">
      <table>
        <tr>
          <th className="item">Item Name</th>
          <th className="date">Transaction Date</th>
          <th className="payer">Who Paid?</th>
          <th className="cost">Cost</th>
        </tr>
        <tr>
          <td className="item">Tomato</td>
          <td className="date">41 Nov 3000</td>
          <td className="payer">Bob</td>
          <td className="cost">$49.34</td>
        </tr>
      </table>
    </div>
  )
}

export default DashboardTable