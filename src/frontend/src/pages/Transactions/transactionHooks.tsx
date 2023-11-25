// import { useState, useEffect } from "react";

// // Get range for pages
// const calculateRange=(data, rowsPerPage)=>{
//     const range=[];
//     const num = Math.ceil(data.length/rowsPerPage);

//     let i=1;
//     for (let i=1; i<=num;i++){
//         range.push(i)
//     }

//     return range
// };

// const sliceData=(data, page, rowsPerPage)=>{
//     // Slice returns a copy of the list ith specific range    
//     // page-1 since index 0 to get first number of page, etc 
//     return data.slice((page-1)*rowsPerPage,page*rowsPerPage)

// }

// const useTable = (data, page, rowsPerPage) => {
//     // Defining states tablRange and slice of elements for current page - set... change the values
//     const [tableRange, setTableRange] = useState([]);
//     const [slice, setSlice] = useState([]);
//     console.log('enter')



//     // if data in [] is changed, calculate range of table and store data in state
//     useEffect(() => {
//         console.log('effectused')
//         const range = calculateRange(data, rowsPerPage);
//         // ... is spread operator to convert array into set of arguments e.g. in a list
//         setTableRange([...range]);
//         console.log(range)
 
//         const slice = sliceData(data, page, rowsPerPage);
//         setSlice([...slice]);
//         console.log(slice)

//         // ...
//       }, [data, setTableRange, page, setSlice]);

//       console.log(slice)
//       console.log(tableRange)

    
//     return { slice, range: tableRange };

// };

// export default useTable;