import "./authentication.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";
import { signIn } from "supertokens-web-js/recipe/emailpassword";
import Cookies from "js-cookie";
import RedExclamation from "./components/red_exclamation";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [invalid_attempt, setAttempt] = useState("valid");
  const navigate = useNavigate();

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const getProfileInfo = () => {
    axios
      .get("http://127.0.0.1:5050/api/user/login_profile", { withCredentials: true })
      .then((res: AxiosResponse) => {
        console.log(res);
        Cookies.set("user_name", res.data["user_name"]);
        Cookies.set("household_name", res.data["household_name"]);
        Cookies.set(
          "household_members",
          JSON.stringify(res.data["household_profile_list"])
        );
        navigate("/page/dashboard");
      })
      .catch((err: AxiosError) => {
        console.log(err);
      });
  };

  async function signInClicked(email: string, password: string) {
    try {
      let response = await signIn({
        formFields: [
          {
            id: "email",
            value: email,
          },
          {
            id: "password",
            value: password,
          },
        ],
      });

      if (response.status === "FIELD_ERROR") {
        response.formFields.forEach((formField) => {
          if (formField.id === "email") {
            // Email validation failed (for example incorrect email syntax).
            window.alert(formField.error);
          }
        });
      } else if (response.status === "WRONG_CREDENTIALS_ERROR") {
        window.alert("Email password combination is incorrect.");
      } else if (response.status === "SIGN_IN_NOT_ALLOWED") {
        // this can happen due to automatic account linking. Tell the user that their
        // input credentials is wrong (so that they do through the password reset flow)
      } else {
        getProfileInfo();
      }
    } catch (err: any) {
      if (err.isSuperTokensGeneralError === true) {
        // this may be a custom error message sent from the API by you.
        window.alert(err.message);
      } else {
        console.log(err);
        setAttempt("invalid");
      }
    }
  }

  const attemptLogin = (e: React.FormEvent) => {
    e.preventDefault();
    signInClicked(email, password);
  };

  return (
    <main className="auth">
      <div className="title">Login to your account</div>
      <div className="whiteBox">
        <form className="loginForm" onSubmit={attemptLogin}>
          <label>
            Email Address <br />
            <input
              type="text"
              id="email"
              value={email}
              onChange={handleEmailChange}
              className={invalid_attempt}
            ></input>
          </label>
          <br />
          {invalid_attempt == "invalid" && (
            <div className="error">
              <RedExclamation></RedExclamation>
              <span className={invalid_attempt}>
                Sorry, we can't find your account!{" "}
              </span>
            </div>
          )}
          <label>
            <span>Password</span>
            <Link to="/recovery" className="forgotPassword">
              Forgot password
            </Link>
            <br />
            <input
              type="password"
              id="password"
              value={password}
              onChange={handlePasswordChange}
            ></input>
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
