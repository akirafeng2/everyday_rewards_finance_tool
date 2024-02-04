import "./authentication.css";
import { Link, useNavigate } from "react-router-dom";
import { signUp } from "supertokens-web-js/recipe/emailpassword";
import { useState } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";
import Cookies from "js-cookie";
import { getUserId } from "supertokens-auth-react/recipe/session";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
  };

  const registerProfile = (user_id: string, name: string) => {
    Cookies.set("user_id", user_id);
    Cookies.set("user_name", name);
    axios
      .post("http://127.0.0.1:5050/api/user/register_profile", {
        user_id: user_id,
        name: name,
      })
      .then(() => {
        navigate("/household/setup");
      })
      .catch((err: AxiosError) => {
        console.log(err);
      });
  };

  async function signUpClicked(email: string, password: string, name: string) {
    try {
      let response = await signUp({
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
        // one of the input formFields failed validaiton
        response.formFields.forEach((formField) => {
          if (formField.id === "email") {
            // Email validation failed (for example incorrect email syntax),
            // or the email is not unique.
            window.alert(formField.error);
          } else if (formField.id === "password") {
            // Password validation failed.
            // Maybe it didn't match the password strength
            window.alert(formField.error);
          }
        });
      } else if (response.status === "SIGN_UP_NOT_ALLOWED") {
        // this can happen during automatic account linking. Tell the user to use another
        // login method, or go through the password reset flow.
      } else {
        // sign up successful. The session tokens are automatically handled by
        // the frontend SDK.
        registerProfile(response.user.id, name);
        console.log(response);
      }
    } catch (err: any) {
      if (err.isSuperTokensGeneralError === true) {
        // this may be a custom error message sent from the API by you.
        window.alert(err.message);
      } else {
        window.alert("Oops! Something went wrong.");
      }
    }
  }

  const attemptSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    signUpClicked(email, password, name);
    // registerProfile(name);
  };
  return (
    <main className="auth">
      <div className="title">Create your account</div>
      <div className="whiteBox">
        <form className="signupForm" onSubmit={attemptSignUp}>
          <label>
            Name <br />
            <input type="text" id="name" onChange={handleNameChange}></input>
          </label>
          <br />
          <label>
            Email Address <br />
            <input type="text" id="email" onChange={handleEmailChange}></input>
          </label>
          <br />
          <label>
            <span>Password</span>
            <br />
            <input
              type="password"
              id="password"
              onChange={handlePasswordChange}
            ></input>
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
