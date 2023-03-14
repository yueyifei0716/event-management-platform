import "./hostreset.css";
import React, { useContext, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import FormInput from "../../components/FormInput/FormInput";
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import instance from '../../utils/axios';
import AuthContext from "../../context/AuthContext";
import { extractHostId } from "../../utils/Token";


const HostReset = () => {

    // initialize the defaut state
    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);
    const [values, setValues] = useState({
        token: token,
        host_id: parseInt(host_id),
        old_password: "",
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
            name: "old_password",
            type: "password",
            placeholder: "Old Password",
            errorMessage:
                "Password should be 6-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label: "Old Password",
            pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*()-_=+{}:"/,./?><';])[a-zA-Z0-9!@#$%^&*()-_=+{}:"/,,./?><';]{6,20}$`,
            required: true,
        },
        {
            id: 2,
            name: "new_password",
            type: "password",
            placeholder: "New Password",
            errorMessage:
                "Password should be 6-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label: "New Password",
            pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*()-_=+{}:"/,./?><';])[a-zA-Z0-9!@#$%^&*()-_=+{}:"/,,./?><';]{6,20}$`,
            required: true,
        },
        {
            id: 3,
            name: "confirm_password",
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/host/resetpassword", values);
            navigate("/host_dashboard");
            setError(false);
            setSuccess(true);
        } catch (err) {
            setError(true);
            setSuccess(false);
        }
    };

    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div className="formContainer2">
                        <div className="formWrapper2">
                            <span className="logo">
                                <img src={require('../../asserts/logo/logo.png')}
                                    alt="" className="topAvatar" />
                                UNeverSleepWell
                            </span>
                            <span className="title">Host Reset Password</span>
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
                                        Reset Successful! You will come back to the dashboard.
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
                                <button className="submit1" type='submit' id="shadowbtn">Reset</button>
                            </form>
                            <Link to="/host_dashboard">
                                <button className="home" id="shadowbtn">Back to home page</button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HostReset