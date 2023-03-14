import "./timeseting.css";
import instance from '../../utils/axios';
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";


const TimePush = () => {
    // setting up the state
    const [inputs, setInputs] = useState({
        week: 0,
        day: 0,
        hour: 0,
        minute: 0,
        second: 0,
    });
    const [err, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setInputs((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    // submit the time to the backend
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/time/push/now", inputs);
            navigate("/");
            setError(false);
            setSuccess(true);
        } catch (err) {
            setError(true);
            setSuccess(false);
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
                <span className="title">Private page : Time pass </span>
                {/* set the time you want to pass */}
                <form onSubmit={handleSubmit}>
                    <input
                        required
                        type="number"
                        min='0'
                        placeholder="week"
                        name="week"

                        onChange={handleChange}
                    />
                    <input
                        required
                        type="number"
                        min='0'
                        placeholder="day"
                        name="day"
                        onChange={handleChange}
                    />
                    <input
                        required
                        type="number"
                        min='0'
                        placeholder="hour"
                        name="hour"
                        onChange={handleChange}
                    />
                    <input
                        required
                        type="number"
                        min='0'
                        placeholder="minute"
                        name="minute"
                        onChange={handleChange}
                    />
                    <input
                        required
                        type="number"
                        min='0'
                        placeholder="second"
                        name="second"
                        onChange={handleChange}
                    />


                    <button class= "setting" id='clmbtn'> Set Time </button>
                </form>
                <Link to="/">
                    <button id='clmbtn' class= "back">Back to home page</button>
                </Link>
            </div>
        </div>
    )
}

export default TimePush