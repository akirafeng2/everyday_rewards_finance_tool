import "./App.css";
import Header from "./components/header";
import SubHeader from "./components/subheader";

function App() {
  return (
    <>
      <div id="main">
        <Header text="Welcome back, Alex 👋" />
        <SubHeader text = "Here's your household expenses summary" />
      </div>
    </>
  );
}

export default App;
