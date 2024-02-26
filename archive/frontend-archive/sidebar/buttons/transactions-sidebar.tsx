
// Enforces type
interface sidebarProps{
    fill: string
}

const  Transaction = ({fill}: sidebarProps) => {
  return (
        <svg width="26" height="19" viewBox="0 0 26 19" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g id="Group 74">
        <path id="Vector" d="M8.25 2H24.5" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <path id="Vector_2" d="M8.25 9.5H24.5" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <path id="Vector_3" d="M8.25 17H24.5" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <path id="Vector_4" d="M2 2.00024H2.01042" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <path id="Vector_5" d="M2 9.5H2.01042" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <path id="Vector_6" d="M2 17H2.01042" stroke={fill} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        </g>
        </svg>
  );
};

export default Transaction;




