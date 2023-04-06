import React, {useState, useContext} from "react";
import SignUp from "./SignUp";
import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";

const baseURL = "http://127.0.0.1:8000"

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrrorMessage] = useState("")
    const [, setToken] = useContext(UserContext)
    const [showSignupModal, setShowSignupModal] = useState(false);
    const [regSuccess, setRegSuccess] = useState(false);

    const submitLogin = async () => {
        const data = new URLSearchParams();
        data.append("username", username)
        data.append("password", password)
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: data,
        }
        const response = await fetch(`${baseURL}/user/sign-in`, requestOptions)
        const answer =  await response.json()
        if (!response.ok) {
            setErrrorMessage("Bad credentials")
        } else {
            setToken(answer.access_token)
        }
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    };

    const showSingUp = () => {
        setShowSignupModal(true)
    }

    const closeSignUp = () => {
        setShowSignupModal(false)
    }

    const showRegSuccess = () => {
        setShowSignupModal(false)
        setRegSuccess(true)
    }

    const closeRegSuccess = () => {
        setRegSuccess(false)
    }

    return (
        <>
        <div className="login-container">
            <div className="about">
                <h1>My<span className="color-text">Site</span></h1>
                <p>MySite helps you to always stay in touch and communicate with your friends.</p>
            </div>
            <div className="login">
                <h1>Log<span className="color-text">in</span></h1>
                <div className="login-form">
                    <form onSubmit={handleSubmit}>
                        <input 
                            type="text"
                            placeholder="email"
                            value={username}
                            onChange={(e) => {
                                setUsername(e.target.value)
                                setErrrorMessage("")
                            }}
                            required
                        />
                        <input
                            type="password"
                            placeholder="password"
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value)
                                setErrrorMessage("")
                            }}
                            required 
                        />
                        <div className="error-container">
                            <a href="#" className="forgot-password">Forgot password?</a>
                            <div className="error-msg">
                                <ErrorMessage message={errorMessage} />
                                {!errorMessage ? <br /> : <></>}
                            </div>
                        </div>
                        <div className="button-group">
                            <button type="submit">Login</button>
                            <button type="button" onClick={showSingUp}>Sign up</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        {showSignupModal && <SignUp onClose={closeSignUp} onSuccess={showRegSuccess}/>}
        {regSuccess && (
            <div class="registration" id="registration">
                <div class="reg-success">
                    <h1>Well<span class="color-text">Come</span></h1>
                    <p>You have successfully registered!</p>
                    <p>Please log in with the above data</p>
                    <button onClick={closeRegSuccess}>Close</button>
                </div>
            </div>
        )}
        </>
    );
};

export default Login;