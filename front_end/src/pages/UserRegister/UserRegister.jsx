import "./userregister.css";
import React, { useContext, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import instance from '../../utils/axios';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import AuthContext from "../../context/AuthContext";
import FormInput from "../../components/FormInput/FormInput";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import { decodeId } from "../../utils/CodingId";
import { wait } from "../../utils/TimeWait";


const UserRegister = () => {

    // initialize the defaut state
    const { setAuthDetail } = useContext(AuthContext);
    const [errMsg, setErrMsg] = useState('');
    const [values, setValues] = useState({
        email: "",
        password: "",
        name_first: "",
        name_last: "",
        address: "",
        bill_method: "",
        account: ""
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
            name: "name_first",
            type: "text",
            placeholder: "First Name",
            errorMessage:
                "The first name is empty!",
            label: "First Name",
            required: true,
        },
        {
            id: 4,
            name: "name_last",
            type: "text",
            placeholder: "Last Name",
            errorMessage:
                "The last name is empty!",
            label: "Last Name",
            required: true,
        },
        {
            id: 5,
            name: "address",
            type: "text",
            placeholder: "Address",
            errorMessage:
                "The address is empty!",
            label: "Address",
            required: true,
        },
    ];

    const wechat_input = {
        id: 6,
        name: "account",
        type: "text",
        placeholder: "Account 3-40 characters",
        errorMessage:
            "The account is invalid! It should be 3-40 characters.",
        label: "Account",
        pattern: `^[a-zA-Z0-9]{3,40}$`,
        required: true,
    }

    const visa_inputs = [
        {
            id: 7,
            name: "name",
            type: "text",
            placeholder: "Name",
            errorMessage: "The name is empty!",
            label: "Name",
            required: true
        },
        {
            id: 8,
            name: "limit_time",
            type: "date",
            placeholder: "Limit Time",
            errorMessage: "The time is empty!",
            label: "Limit Time",
            required: true,
        },
        {
            id: 9,
            name: "account",
            type: "text",
            placeholder: "Account Number",
            errorMessage:
                "The account is invalid! It should be 16 digits",
            label: "Account Number 16 digits",
            pattern: `^[0-9]{16}$`,
            required: true
        },
        {
            id: 10,
            name: "csv",
            type: "text",
            placeholder: "CSV 3 digits",
            errorMessage:
                "The CSV code is invalid! You should enter 3 digits",
            label: "CSV ",
            pattern: `^[0-9]{3}$`,
            required: true
        },
    ];

    const bpay_inputs = [
        {
            id: 11,
            name: "name",
            type: "text",
            placeholder: "Name",
            errorMessage: "The name is empty!",
            label: "Name",
            required: true
        },
        {
            id: 12,
            name: "bsb",
            type: "text",
            placeholder: "BSB  6 digits",
            errorMessage: "The bsb is invalid! You should enter 6 digits",
            label: "BSB",
            pattern: `^[0-9]{6}$`,
            required: true
        },
        {
            id: 13,
            name: "account",
            type: "text",
            placeholder: "Account Number 8 digits",
            errorMessage:
                "The account is invalid! You should enter 8 digits",
            label: "Account Number",
            pattern: `^[0-9]{8}$`,
            required: true
        },
    ];

    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (values.bill_method === "visa") {
                await instance.post("/time/check", { time: values.limit_time });
            }
            const res = await instance.post("/user/signup", values);
            const token = res.data.token;
            const user_id = decodeId(res.data.user_id);
            const host_id = '';
            setAuthDetail(token, user_id, host_id);
            setSuccess(true);
            wait(1000);
            navigate("/user_dashboard");
        } catch (err) {
            setError(true)
            if (!err.response) {
                setErrMsg('No Server Response!');
            } else {
                setErrMsg('Email already exists!');
            }
        }
    };

    const renderSelection = (method) => {
        switch (method) {
            case "wechat":
                return (
                    <FormInput
                        key={wechat_input.id}
                        {...wechat_input}
                        value={values[wechat_input.name]}
                        onChange={handleChange}
                    />
                )
            case "visa":
                return (
                    visa_inputs.map((input) => (
                        <FormInput
                            key={input.id}
                            {...input}
                            value={values[input.name]}
                            onChange={handleChange}
                        />
                    ))
                )
            case "bpay":
                return (
                    bpay_inputs.map((input) => (
                        <FormInput
                            key={input.id}
                            {...input}
                            value={values[input.name]}
                            onChange={handleChange}
                        />
                    ))
                )
        }
    }

    return (

        <div className="formContainer4">
            <div></div>
            <div className="formWrapper2">
                <span className="logo">
                    <img src={require('../../asserts/logo/logo.png')}
                        alt="" className="topAvatar" />
                    UNeverSleepWell
                </span>
                <span className="title">User Sign Up</span>
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
                            Sign up Successful! You will be redirect to the dashboard.
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
                    <FormControl>
                        <FormLabel id="demo-radio-buttons-group-label">Bill Method</FormLabel>
                        <RadioGroup
                            row
                            aria-labelledby="demo-row-radio-buttons-group-label"
                            name="bill_method"
                            onChange={handleChange}
                        >
                            <FormControlLabel value="wechat" control={<Radio />} label="WeChat" />
                            <FormControlLabel value="visa" control={<Radio />} label="Visa" />
                            <FormControlLabel value="bpay" control={<Radio />} label="Bpay" />
                        </RadioGroup>
                    </FormControl>
                    {renderSelection(values.bill_method)}
                    <button className="userSign" type='submit' id="shadowbtn">Sign Up</button>
                </form>
                <p>You already have an account? <Link to="/user_login">Login</Link></p>
                <Link to="/">
                    <button className="home" id="shadowbtn">Back to home page</button>
                </Link>
            </div>
        </div>

    )
}

export default UserRegister