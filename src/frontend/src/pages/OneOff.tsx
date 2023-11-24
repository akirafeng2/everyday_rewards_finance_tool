import Header from "../components/header";
import SubHeader from "../components/subheader";


function OneOff() {
  return (
    <>
      <div id="main">
        <Header text="Imported Transaction History" />
        <SubHeader text = "start date dd/mm/yyyy" />
        Oneoff!
      </div>
    </>
  );
}
  
export default OneOff;