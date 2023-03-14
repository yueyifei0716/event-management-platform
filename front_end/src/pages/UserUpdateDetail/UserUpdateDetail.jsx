import "./UserUpdateDetail.css";
import instance from '../../utils/axios';
import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import FormInput from "../../components/FormInput/FormInput";
import { extractUserId } from "../../utils/Token";
import Topbar from "../../components/TopBar/UserTopBar";
import Sidebar from "../../components/SideBar/UserSideBar";


const UserUpdateDetail = () => {

    // initialize the defaut state
    const [values, setValues] = useState({
        first_name: "",
        last_name: "",
        address: "",
    });
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const navigate = useNavigate();

    // define the parameters of the input boxes in the form
    const inputs = [
        {
            id: 1,
            name: "first name",
            type: "text",
            placeholder: "first name",
            errorMessage: "cannot be empty!",
            label: "first name",
            required: true,
        },
        {
            id: 2,
            name: "last name",
            type: "text",
            placeholder: "last name",
            errorMessage: "cannot be empty!",
            label: "last name",
            required: true,
        },
        {
            id: 3,
            name: "address",
            type: "text",
            placeholder: "address",
            errorMessage: "cannot be empty!",
            label: "address",
            required: true,
        },
    ];

    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const first_name = e.target[0].value;
        const last_name = e.target[1].value;
        const address = e.target[2].value;
        try {
            await instance.post("/user/detailupdate", { user_id: user_id, token: token, first_name: first_name, last_name: last_name, address: address });
            navigate("/user_detail");
        } catch (err) {}
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
                            <span className="title">User update detail</span>
                            <form onSubmit={handleSubmit}>
                                {inputs.map((input) => (
                                    <FormInput
                                        key={input.id}
                                        {...input}
                                        value={values[input.name]}
                                        onChange={handleChange}
                                    />
                                ))}
                                <button id="shadowbtn" className="update" type='submit'>Update</button>

                            </form>
                            <div className='btns'>
                                <Link style={{ textDecorationLine: 'none' }} to="/user_detail">
                                    <button id="shadowbtn" className="home">Back to home page</button>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )

}

export default UserUpdateDetail