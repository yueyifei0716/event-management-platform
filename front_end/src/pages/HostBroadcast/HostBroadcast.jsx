import "./HostBroadcast.css";
import instance from '../../utils/axios';
import React, { useContext, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import FormInput from "../../components/FormInput/FormInput";
import { extractHostId } from "../../utils/Token";
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";

const HostBroadcast = () => {

    // get the activity id from the previous page's state
    const navigate = useNavigate();
    const location = useLocation();
    const { activity_id } = location.state;
    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);

    // initialize the defaut state
    const [values, setValues] = useState({
        host_id: parseInt(host_id),
        activity_id: activity_id,
        message: "",
        token: token,
    });
    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);

    // define the parameters of the input boxes in the form
    const inputs = [
        {
            id: 1,
            name: "message",
            type: "text",
            placeholder: "message",
            errorMessage: "cannot be empty!",
            label: "message",
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
            await instance.post("/host/broadcast", values);
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
                        <div className="formWrapper">
                            <span className="logo">UNeverSleepWell</span>
                            <span className="title">Host broadcast</span>
                            <form onSubmit={handleSubmit}>
                                {inputs.map((input) => (
                                    <FormInput
                                        key={input.id}
                                        {...input}
                                        value={values[input.name]}
                                        onChange={handleChange}
                                    />
                                ))}
                                <button className="boradcast" id="shadowbtn" type='submit'>Broadcast</button>
                            </form>
                            <Link to="/host_activity_list">
                                <button className="home4" id="shadowbtn">Back</button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HostBroadcast