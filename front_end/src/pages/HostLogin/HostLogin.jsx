import "./hostlogin.css";
import instance from '../../utils/axios';
import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import FormInput from "../../components/FormInput/FormInput";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import { decodeId } from "../../utils/CodingId";
import { wait } from "../../utils/TimeWait";


const HostLogin = () => {

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
    ];

    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await instance.post('/host/login', values);
            const token = res.data.token;
            const user_id = '';
            const host_id = decodeId(res.data.host_id);
            setAuthDetail(token, user_id, host_id);
            setSuccess(true);
            wait(1000);
            navigate("/host_dashboard");
        } catch (err) {
            setError(true)
            if (!err.response) {
                setErrMsg('No Server Response!');
            } else {
                setErrMsg('Login Failed!');
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
                <span className="title">Host Login</span>
                <form onSubmit={handleSubmit}>
                    {error && (
                        <Alert severity="error">
                            <AlertTitle>Error</AlertTitle>
                            The <strong>email</strong> or <strong>password</strong> you entered <br></br>
                            may not exist or may be incorrect.
                            <strong>{errMsg}</strong>
                        </Alert>
                    )}
                    {success && (
                        <Alert severity="success">
                            <AlertTitle>Success</AlertTitle>
                            Login Successful! You will be redirect to the dashboard.
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
                    <button className="Login" type='submit' id="shadowbtn">Login</button>
                </form>
                <p>You don't have an account? <Link to="/host_register" >Sign Up</Link></p>
                <p className="link-text">Forgot your password? <Link to="/host_forget">Reset Password</Link></p>
                <Link to="/">
                    <button className="home" id="shadowbtn">Back to home page</button>
                </Link>
            </div>
        </div>
    )
}

export default HostLogin