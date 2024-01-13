import Header from "../../components/headers/header";
import SubHeader from "../../components/headers/subheader";
import './transactions.css'
import TransactionRow from "./transactionRow";

// import useTable from "./transactionHooks";
import TableFooter from "./tableFooter";
import Delete from '../../assets/bin.svg';
import Filter from '../../assets/filter.svg';
import Export from '../../assets/export.svg';
import Down from '../../assets/down.svg'
import Up from '../../assets/up.svg'
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

// Reverse the data list 
const reverse=(data)=>{
  return data.reverse();
}

function Transactions() {

  const tableDataManual=[
    {
      Id: '1',
      Date:'10 Dec 2020',
      Name: 'Butter', 
      Cost: '$4.00',
      Paid: 'Alex'
    },
    {
      Id:'2',
      Date:'10 Dec 2020',
      Name: 'Milk',
      Cost: '$2.00',
      Paid: 'Adam'
    },
    {
      Id: '3',
      Date:'10 Dec 2020',
      Name: 'Egg',
      Cost: '$6.20',
      Paid: 'Tyler' 
    },
    {
      Id: '4',
      Date:'13 Dec 2020',
      Name: 'MORE Butter', 
      Cost: '$4.00',
      Paid: 'Alex'
    },
    { 
      Id:'5',
      Date:'13 Dec 2020',
      Name: 'MORE Milk',
      Cost: '$2.00',
      Paid: 'Adam'
    },
    {
      Id: '6',
      Date:'13 Dec 2020',
      Name: 'MORE Egg',
      Cost: '$6.20',
      Paid: 'Tyler' 
    }
  ]
    const [sort, setSort] = useState('asc');
    const [data, setData] = useState(tableDataManual)
    const rowsPerPage=2
    const lastPage = Math.ceil(data.length/rowsPerPage)
    const [tableRange, setTableRange] = useState([]);
    const [slice, setSlice] = useState([]);
    const [page, setPage] = useState(1);
    


    useEffect(() => { 
      console.log('effectused')
      const range = calculateRange(data, rowsPerPage);
      // ... is spread operator to convert array into set of arguments e.g. in a list
      setTableRange([...range]);
      console.log(range)
 
      const slice = sliceData(data, page, rowsPerPage);
      setSlice([...slice]);
      console.log(slice)

      // should trigger if page
    }, [ page]);

    useEffect(() => {
      console.log('entered reversal')
      setData(reverse(data))

      const range = calculateRange(data, rowsPerPage);
      // ... is spread operator to convert array into set of arguments e.g. in a list
      setTableRange([...range]);
      console.log(range)
 
      const slice = sliceData(data, page, rowsPerPage);
      setSlice([...slice]);
    }, [sort])
  
    


    // Creates a list of Transaction rows. The Map maps the items 
    //form the entries in tableDataManuel to the kth item in transactionsList?
    const transactionsList = Object.entries(slice).map(function(item, k) { 
       return <TransactionRow  args={item[1]}/>
    })


    var imgSort = (<img className='transactionsSort'src={Down} onClick={() => setSort(sort==='asc'? 'desc': 'asc')}></img>)
    if (sort=='desc'){
      imgSort=<img className='transactionsSort'src={Up} onClick={() => setSort(sort==='asc'? 'desc': 'asc')}></img>

    }




 
  return (
    <>
      <div className="main">
        <Header text="Imported Transaction History" />
        <SubHeader text = "start date dd/mm/yyyy" />

        <div className='tableFunctionalities'>
          June 2023  {/* Need to change so dyamic for month */}
   
          <div className="functionsRight">
            <button className='tableChange'>
              <img src={Delete}></img>
              Delete
              </button>
            <button className='tableChange'>
              <img src={Filter}></img>
              Filter
              </button>
              <button className='exportButton'>
              <img src={Export}></img>
              Export
              </button>
              <button className='uploadRewards'>
              + Upload Everyday Rewards
              </button>
          </div>
        </div >

        <div className='tableData'>
            <table id="transactionsTable">
              <thead>
                <tr id="transactionsTableHeader">
                      <th>Checkbox</th>
                      <th>
                        <div id='transactionDateDiv'>
                        Transaction Date
                        {imgSort}
                        </div>
                      </th>
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
        <TableFooter lastPage={lastPage} range={tableRange} slice={slice} setPage={setPage} page={page} />

      </div>
    </>
  );
}
  
export default Transactions;
