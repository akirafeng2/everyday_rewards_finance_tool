// Enforces type
interface sidebarProps{
    fill: string
}

const  OneOff = ({fill}: sidebarProps) => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="27" height="24" viewBox="0 0 27 24" fill="none">
    <path d="M1.31885 7.72174H25.2622" stroke={fill} stroke-width="2.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M6.10742 17.4764H8.50175" stroke={fill} stroke-width="2.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M11.4946 17.4764H16.2833" stroke={fill} stroke-width="2.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M6.63378 1.625H19.9343C24.1962 1.625 25.2617 2.69802 25.2617 6.97789V16.9887C25.2617 21.2685 24.1962 22.3415 19.9463 22.3415H6.63378C2.38384 22.3537 1.31836 21.2807 1.31836 17.0009V6.97789C1.31836 2.69802 2.38384 1.625 6.63378 1.625Z" stroke={fill} stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  );
};

export default OneOff;
