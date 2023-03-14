import "./hostregister.css";
import React, { useContext, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import instance from '../../utils/axios';
import FormInput from "../../components/FormInput/FormInput";
import AuthContext from "../../context/AuthContext";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import { decodeId } from "../../utils/CodingId";


const HostRegister = () => {

    // initialize the defaut state
    const { setAuthDetail } = useContext(AuthContext);
    const [errMsg, setErrMsg] = useState('');
    const [values, setValues] = useState({
        email: "",
        password: "",
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
            name: "password",
            type: "password",
            placeholder: "Password",
            errorMessage:
                "Password should be 6-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label: "Password",
            pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_=+{}:"/,./?><';])[a-zA-Z0-9!@#$%^&*()_=+{}:"/,,./?><';]{6,20}$`,
            required: true,
        },
        {
            id: 3,
            name: "confirmPassword",
            type: "password",
            placeholder: "Confirm Password",
            errorMessage: "Passwords don't match!",
            label: "Confirm Password",
            pattern: values.password,
            required: true,
        },
    ];


    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await instance.post("/host/signup", values);
            const token = res.data.token;
            const user_id = '';
            const host_id = decodeId(res.data.host_id);
            setAuthDetail(token, user_id, host_id);
            setSuccess(true);
            navigate("/host_dashboard");
        } catch (err) {
            setError(true)
            if (!err.response) {
                setErrMsg('No Server Response!');
            } else {
                setErrMsg('Sign up Failed!');
            }
        }
    };

    return (
        <div className="formContainer2">
            <div className="formWrapper2">
                <span className="logo">
                    <img src={require('../../asserts/logo/logo.png')}
                        alt="" className="topAvatar" />
                    UNeverSleepWell

                </span>
                <span className="title">Host Sign Up</span>
                <form onSubmit={handleSubmit}>
                    {error && (
                        <Alert severity="error">
                            <AlertTitle>Error</AlertTitle>
                            The <strong>email</strong> is already taken — <strong>{errMsg}</strong>
                        </Alert>
                    )}
                    {success && (
                        <Alert severity="success">
                            <AlertTitle>Success</AlertTitle>
                            Register Successful! You will be redirect to the dashboard.
                        </Alert>
                    )}

                    {inputs.map((input) => (
                        <FormInput
                            key={input.id}
                            {...input}
                            value={values[input.name]}
                            onChange={handleChange}
                        />
                    ))}
                    <button className="Register" type='submit' id="shadowbtn">Sign Up</button>
                </form>
                <p>You already have an account? <Link to="/host_login">Login</Link></p>
                <Link to="/">
                    <button className="home" id="shadowbtn">Back to home page</button>
                </Link>
            </div>
        </div>
    )
}

export default HostRegister