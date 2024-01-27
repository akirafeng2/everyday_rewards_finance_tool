import "./authentication.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const attemptLogin = (e: React.FormEvent) => {
    e.preventDefault();

    axios.post("http://127.0.0.1:5050/api/user/login", {
        email: email,
        password: password,
      })
      .then((res: AxiosResponse) => {
        console.log(res);
        navigate('/page/dashboard')
      })
      .catch((err: AxiosError) => {
        console.log(err);
      });
  };

  return (
    <main className="auth">
      <div className="title">Login to your account</div>
      <div className="whiteBox">
        <form className="loginForm" onSubmit={attemptLogin}>
          <label>
            Email Address <br />
            <input type="text" id="email" value={email} onChange={handleEmailChange}></input>
          </label>
          <br />
          <label>
            <span>Password</span>
            <Link to="/recovery" className="forgotPassword">
              Forgot password
            </Link>
            <br />
            <input type="password" id="password" value={password} onChange={handlePasswordChange}></input>
          </label>
          <br />
          <input type="submit" value="Log In" className="button"></input>
          <br />
          <label className="swap">
            <span>Don't have an account? </span>
            <Link to="/signup" className="here">
              Sign up here
            </Link>
          </label>
        </form>
      </div>
    </main>
  );
}

export default Login;
