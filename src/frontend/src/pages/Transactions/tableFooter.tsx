import React, { useEffect } from "react";
import leftArrow from '../../assets/leftArrow.svg'
import rightArrow from '../../assets/rightArrow.svg'

import './transactions.css'
const TableFooter = ({ lastPage, range, setPage, page, slice }) => {


  return (

    <div className='tableFooter'>
        {/* The left arrow */}

        <button>
            <img src={leftArrow} onClick={() => setPage((page==1? 1:page-1)) }></img>
        </button>

      {range.map((el, index) => (
        
        // for each element in the range, create a button
        // key is the index and classsname
        <button
          key={index}
          // classname is .button, but if index is current page, the style becomes activebutton, else inactive button
          className={ (page === el ? 'activeButton' : 'inactiveButton')}

          // oClick, we run the setPage function to the element
          onClick={() => setPage(el)}
        >
          {el}
        </button>

      ))}
        {/* the right arrow */}
        <button  onClick={() => setPage((page===lastPage ?lastPage :page+1))}>
            <img src={rightArrow}></img>
        </button>
    </div>  );
};

export default TableFooter;