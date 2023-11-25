import React, { useEffect } from "react";

import './transactions.css'
const TableFooter = ({ range, setPage, page, slice }) => {
    // when slice, page or setPage changes and no more elements, make it the last page
  useEffect(() => {
    if (slice.length < 1 && page !== 1) {
      setPage(page - 1);
    }
  }, [slice, page, setPage]);

  return (

    <div className='tableFooter'>
      {range.map((el, index) => (
        
        // for each element in the range, create a button
        // key is the index and classsname
        <button
          key={index}
          // classname is .button, but if index is current page, the style becomes activebutton, else inactive button
          className={'button' + (page === el ? 'activeButton' : 'inactiveButton')}

          // oClick, we run the setPage function to the element
          onClick={() => setPage(el)}
        >
            // page number as text
          {el}
        </button>

      ))}
    </div>  );
};

export default TableFooter;