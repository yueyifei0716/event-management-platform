import "./UserEditAccount.css";
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
import { extractUserId } from "../../utils/Token";
import { wait } from "../../utils/TimeWait";


const UserEditAccount = () => {

    // initialize the defaut state
    const [errMsg, setErrMsg] = useState('');
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const [values, setValues] = useState({
        user_id: "",
        bill_method: "",
        account: "",
        token: ""
    });
    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    // define the parameters of the input boxes in the form
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
            placeholder: "Account Number (16 digits)",
            errorMessage:
                "The account is invalid!  You need to input 16 digits",
            label: "Account Number",
            pattern: `^[0-9]{16}$`,
            required: true,
        },
        {
            id: 10,
            name: "csv",
            type: "text",
            placeholder: "CSV 3 digits",
            errorMessage:
                "The CSV code is invalid! You need to input 3 digits",
            label: "CSV",
            pattern: `^[0-9]{3}$`,
            required: true,
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
            required: true,
        },
        {
            id: 12,
            name: "bsb",
            type: "text",
            placeholder: "BSB 6 digits",
            errorMessage: "The bsb is invalid! You need to input 6 digits",
            label: "BSB",
            pattern: `^[0-9]{6}$`,
            required: true,
        },
        {
            id: 13,
            name: "account",
            type: "text",
            placeholder: "Account Number 8 digits",
            errorMessage:
                "The account is invalid! You need to input 8 digits",
            label: "Account Number",
            pattern: `^[0-9]{8}$`,
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
            if (values.bill_method === "visa") {
                await instance.post("/time/check", { time: values.limit_time });
            }
            values.token = token;
            values.user_id = user_id;
            await instance.post("/user/editaccount", values);
            setSuccess(true);
            wait(1000);
            navigate("/user_dashboard");
        } catch (err) {
            setError(true)
            if (!err.response) {
                setErrMsg('No Server Response!');
            } else {
                setErrMsg('fail to edit account!');
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
                console.log('is bpay')
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
        <div className="formContainer3" style={{ paddingTop: "64px", }}>
            <div></div>
            <div className="formWrapper2">
                <span className="logo">
                    <img src={require('../../asserts/logo/logo.png')}
                        alt="" className="topAvatar" />
                    UNeverSleepWell
                </span>
                <span className="title">User edit account</span>
                <form onSubmit={handleSubmit}>
                    {error &&
                        <div className="error">
                            {errMsg}
                        </div>
                    }
                    {success &&
                        <div className="success">
                            successfully!
                        </div>
                    }
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
                    <button className="submit3" type='submit' id="shadowbtn">  Edit</button>
                </form>
                <Link to="/user_detail">
                    <button className="home" id="shadowbtn">Back to home page</button>
                </Link>
            </div>
        </div>

    )
}

export default UserEditAccount