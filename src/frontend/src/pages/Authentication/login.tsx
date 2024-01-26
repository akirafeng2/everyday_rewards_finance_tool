import "./authentication.css";
import { Link } from 'react-router-dom';

function Login() {
  return (
    <main className="auth">
      <div className="title">Login to your account</div>
      <div className="whiteBox">
        <form className="loginForm">
          <label>Email Address <br/>
            <input type="text" id="email"></input>
          </label>
          <br/>
          <label>
            <span>Password</span>
            <Link to="/recovery" className="forgotPassword">Forgot password</Link>
             <br/>
            <input type="secret" id="password"></input>
          </label>
          <br/>
          <input type="submit" value="Log In" className="button"></input>
          <br/>
          <label className="swap">
          <span>Don't have an account?  </span>
          <Link to="/signup" className="here">Sign up here</Link>
          </label>
        </form>
      </div>
    </main>
  );
}

export default Login;
