import Header from "../components/header";
import SubHeader from "../components/subheader";
import './transactions.css'


function Transactions() {
  return (
    <>
      <div id="main">
        <Header text="Imported Transaction History" />
        <SubHeader text = "start date dd/mm/yyyy" />

      </div>
    </>
  );
}
  
export default Transactions;