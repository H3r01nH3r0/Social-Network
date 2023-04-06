import React, { useState } from "react";
import ErrorMessage from "./ErrorMessage";

const baseURL = "http://127.0.0.1:8000"

const SignUp = ({ onClose, onSuccess }) => {
    const [email, setEmail] = useState("");
    const [firstname, setFirstName] = useState("");
    const [lastname, setLastName] = useState("");
    const [birthdate, setBirthDate] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrrorMessage] = useState("")

    const submitSignUp = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, first_name: firstname, last_name: lastname, password: password, birth_date: birthdate }),
        }
        console.log(requestOptions)
        const response = await fetch(`${baseURL}/user/sign-up`, requestOptions)
        const answer =  await response.json()
        if (!response.ok) {
            setErrrorMessage(answer.detail)
        } else {
            onSuccess()
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        submitSignUp();
    };

    const closeSingUp = () => {
        onClose();
    };


    return (
        <div className="modal">
            <div className="modal-container">
                <span className="close" onClick={closeSingUp}>&times;</span>
                <h1>Sign<span className="color-text">Up</span></h1>
                <form onSubmit={handleSubmit}>
                    <div className="input-row">
                        <input 
                            type="text" 
                            placeholder="First name"
                            value={firstname}
                            onChange={(e) => setFirstName(e.target.value)}
                            required
                        />
                        <input
                            type="text" 
                            placeholder="Last name"
                            value={lastname}
                            onChange={(e) => setLastName(e.target.value)}
                            required
                        />
                    </div>
                    <input
                        type="email"
                        placeholder="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <label htmlFor="birth-date">Choose your birth date:</label>
                    <input
                        id="birth-date"
                        type="date" 
                        placeholder="Birth date"
                        value={birthdate}
                        onChange={(e) => setBirthDate(e.target.value)}
                        required
                    />
                    <div className="error-msg">
                        <ErrorMessage message={errorMessage}/>
                        {!errorMessage ? <br />: <></>}
                    </div>
                    <button type="submit">Sign Up</button>
                </form>
            </div>
        </div>
    )
}

export default SignUp;