import "./authentication.css";
import { Link } from "react-router-dom";

function Signup() {
  return (
    <main className="auth">
      <div className="title">Create your account</div>
      <div className="whiteBox">
        <form className="signupForm">
          <label>
            Name <br />
            <input type="text" id="name"></input>
          </label>
          <br />
          <label>
            Email Address <br />
            <input type="text" id="email"></input>
          </label>
          <br />
          <label>
            <span>Password</span>
            <br />
            <input type="secret" id="password"></input>
          </label>
          <br />
          <input type="submit" value="Sign Up" className="button"></input>
          <br />
          <label className="swap">
            <span>Have an account? </span>
            <Link to="/login" className="here">
              Log in here
            </Link>
          </label>
        </form>
      </div>
    </main>
  );
}

export default Signup;
