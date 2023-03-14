import "./timeseting.css";
import instance from '../../utils/axios';
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";


const HostLogin = () => {
    // setting up the state
    const [inputs, setInputs] = useState({
        time: "",
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setInputs((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    // submit the time to the backend
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("http://127.0.0.1:5000/time/set/now", inputs);
            navigate("/");
        } catch (err) {

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
                <span className="title">Private page : Set a new TIME</span>
                <form onSubmit={handleSubmit}>
                    {/* date will  be set Accurate to the second. */}
                    <input
                        required
                        type="datetime-local"
                        step="1"
                        placeholder="set a new Time"
                        name="time"
                        onChange={handleChange}
                    />

                    <button class= "setting" id='clmbtn'> Set Time </button>
                </form>
                <Link to="/">
                    <button id='clmbtn' class= "back"> Back to home page </button>
                </Link>
            </div>
        </div>
    )
}

export default HostLogin