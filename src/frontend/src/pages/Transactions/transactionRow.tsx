import './transactions.css'

interface argsProps{
    Id: string,
    Date: string,
    Name:string,
    Cost:string,
    Paid:string
}

// TODO: Need to pull weightings from weightings page! Is this via api or does daata have weights>?
function TransactionRow({args}: argsProps){
    const Id = args['Id']
    const Date = args['Date']
    const Name = args['Name']
    const Cost = args['Cost']
    const Paid = args['Paid']


    return (
        <tr>
            <td>
                <input type="checkbox" id={Id}/> 
            </td>
            <td>
               {Date}
            </td>
            <td>
                {Name}
            </td>
            <td>
                {Cost}
            </td>
            <td>
                {Paid}
            </td>
            <td className="percentageSplit">
                0.33
            </td>
            <td>
                0.33
            </td>
            <td>
                0.33
            </td>
        </tr>
      );

};

export default TransactionRow;