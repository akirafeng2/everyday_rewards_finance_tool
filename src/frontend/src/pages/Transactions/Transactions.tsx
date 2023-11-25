import Header from "../../components/header";
import SubHeader from "../../components/subheader";
import './transactions.css'
import TransactionRow from "./transactionRow";

// import useTable from "./transactionHooks";
import TableFooter from "./tableFooter";

import { useState, useEffect } from "react";


// Get range for pages
const calculateRange=(data, rowsPerPage)=>{
  const range=[];
  const num = Math.ceil(data.length/rowsPerPage);

  let i=1;
  for (let i=1; i<=num;i++){
      range.push(i)
  }

  return range
};

const sliceData=(data, page, rowsPerPage)=>{
  // Slice returns a copy of the list ith specific range    
  // page-1 since index 0 to get first number of page, etc 
  return data.slice((page-1)*rowsPerPage,page*rowsPerPage)

}

function Transactions() {

  const tableDataManual=[
    {
      Id: '1',
      Date:'13 Dec 2020',
      Name: 'Butter', 
      Cost: '$4.00',
      Paid: 'Alex'
    },
    {
      Id:'2',
      Date:'13 Dec 2020',
      Name: 'Milk',
      Cost: '$2.00',
      Paid: 'Adam'
    },
    {
      Id: '3',
      Date:'13 Dec 2020',
      Name: 'Egg',
      Cost: '$6.20',
      Paid: 'Tyler' 
    },
    {
      Id: '1',
      Date:'13 Dec 2020',
      Name: 'Butter', 
      Cost: '$4.00',
      Paid: 'Alex'
    },
    {
      Id:'2',
      Date:'13 Dec 2020',
      Name: 'Milk',
      Cost: '$2.00',
      Paid: 'Adam'
    },
    {
      Id: '3',
      Date:'13 Dec 2020',
      Name: 'Egg',
      Cost: '$6.20',
      Paid: 'Tyler' 
    }
  ]

    const rowsPerPage=2
    const [tableRange, setTableRange] = useState([]);
    const [slice, setSlice] = useState([]);
    const [page, setPage] = useState(1);


    useEffect(() => { 
      console.log('effectused')
      const range = calculateRange(tableDataManual, rowsPerPage);
      // ... is spread operator to convert array into set of arguments e.g. in a list
      setTableRange([...range]);
      console.log(range)
 
      const slice = sliceData(tableDataManual, page, rowsPerPage);
      setSlice([...slice]);
      console.log(slice)

      // ...
    }, [ page]);

 

    console.log(page)
    // const { slice, range } = useTable(tableDataManual, page, 2);
    console.log(slice)
    console.log(tableRange)
    console.log('hi')

    // Creates a list of Transaction rows. The Map maps the items 
    //form the entries in tableDataManuel to the kth item in transactionsList?
    const transactionsList = Object.entries(slice).map(function(item, k) { 
       return <TransactionRow  args={item[1]}/>
    })


 
  return (
    <>
      <div id="main">
        <Header text="Imported Transaction History" />
        <SubHeader text = "start date dd/mm/yyyy" />

        <div className='tableFunctionalities'>
          June 2023  {/* Need to change so dyamic for month */}
        </div>

        <div className='tableData'>
            <table id="transactionsTable">
              <thead>
                <tr id="transactionsTableHeader">
                      <th>Checkbox</th>
                      <th>Transaction Date</th>
                      <th>Item Name</th>

                      <th>Cost</th>
                      <th>Who Paid?</th>
                      {/* Need to get variable of number of households and household people names */}
                      <th>Alex</th>
                      <th>Adam</th>
                      <th>Tyler</th>

                  </tr>
              </thead>
              <tbody>
                  {transactionsList}
              </tbody>
            </table>
        </div>
        <TableFooter range={tableRange} slice={slice} setPage={setPage} page={page} />

      </div>
    </>
  );
}
  
export default Transactions;
