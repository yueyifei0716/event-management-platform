import "./hostforget.css";
import instance from '../../utils/axios';
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import FormInput from "../../components/FormInput/FormInput";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';


const HostForget = () => {

    // initialize the defaut state
    const [values, setValues] = useState({
        email: "",
        validation: "",
        new_password: "",
        confirm_password: "",
    });
    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    // define the parameters of the input boxes in the form
    const inputs = [
        {
            id: 1,
            name: "email",
            type: "email",
            placeholder: "Email",
            errorMessage: "It should be a valid email address!",
            label: "Email",
            required: true,
        },
        {
            id: 2,
            name: "validation",
            type: "text",
            placeholder: "Validation Code",
            errorMessage:
                "The invalid validation code format",
            label: "Validation Code",
            required: true,
        },
        {
            id: 3,
            name: "new_password",
            type: "password",
            placeholder: "New Password",
            errorMessage:
                "Password should be 6-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label: "New Password",
            pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_=+{}:"/,./?><';])[a-zA-Z0-9!@#$%^&*()_=+{}:"/,,./?><';]{6,20}$`,
            required: true,
        },
        {
            id: 4,
            name: "confirmPassword",
            type: "password",
            placeholder: "Confirm Password",
            errorMessage: "Passwords don't match!",
            label: "Confirm Password",
            pattern: values.new_password,
            required: true,
        },
    ];

    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const onSend = async (e) => {
        await instance.post("/sendemail", { email: values.email });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/host/forgetpassword", values);
            navigate("/host_login");
            setError(false);
            setSuccess(true);
        } catch (err) {
            setError(true);
            setSuccess(false);
        }
    };

    return (
        <div className="formContainer3">
            <div className="formWrapper2">
                <span className="logo">
                    <img src={require('../../asserts/logo/logo.png')}
                        alt="" className="topAvatar" />
                    UNeverSleepWell
                </span>
                <span className="title">Host Forget Password</span>
                <form onSubmit={handleSubmit}>
                    {error && (
                        <Alert severity="error">
                            <AlertTitle>Error</AlertTitle>
                            The <strong>email</strong> or <strong>password</strong> you entered <br></br>
                            may not exist or may be incorrect.
                        </Alert>
                    )}
                    {success && (
                        <Alert severity="success">
                            <AlertTitle>Success</AlertTitle>
                            Reset Successful! You can login by new password now.
                        </Alert>
                    )}

                    {inputs.map((input) => {
                        if (input.name !== "email") {
                            return (
                                <FormInput
                                    key={input.id}
                                    {...input}
                                    value={values[input.name]}
                                    onChange={handleChange}
                                />
                            )
                        }
                        return (
                            <>
                                <FormInput
                                    key={input.id}
                                    {...input}
                                    value={values[input.name]}
                                    onChange={handleChange}
                                />
                                <button className="code" id="shadowbtn" onClick={onSend}>Send validation code</button>
                            </>
                        )
                    })}
                    <button className="forget" type='submit' id="shadowbtn">Reset Password</button>
                </form>
                <p>You don't have an account? <Link to="/host_register">Sign Up</Link></p>
                <Link to="/">
                    <button className="home" id="shadowbtn">Back to home page</button>
                </Link>
            </div>
        </div>
    )
}

export default HostForget