import "./topbar.css";
import React, { useContext, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import instance from '../../utils/axios';
import AuthContext from "../../context/AuthContext";
import { extractHostId } from "../../utils/Token";


// the host top bar
export default function Topbar() {
    const navigate = useNavigate();
    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);
    const [name, setName] = useState('')

    const handleLogout = async (e) => {
        e.preventDefault();
        await instance.post("/host/logout", { host_id, token });
        // after logout, remove the token and corresponding id in the localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("host_id");
        navigate("/");
    };

    // get the name of the user
    useEffect(() => {
        getName()
    }, [])

    const getName = () => {
        let params = {
            host_id: host_id,
        }
        instance.post("/host/name", params).then(res => {
            let name = res.data.name || []
            setName(name)
        })
    }

    return (
        <div className="topbar">
            <div className="topbarWrapper">
                <div className="topLeft">
                    <span className="logo">
                        <img src= {require('../../asserts/logo/logo.png')}
                         alt="" className="topAvatar" />
                         UNeverSleepWell
                    </span>
                </div>
                <div className="topRight">
                    <Link to="/">
                        <button className="navButton" onClick={handleLogout} color = 'error'>Logout</button>
                    </Link>
                    <span className="email"> { name } </span>
                    <img src= {require('../../asserts/logo/my.jpg')}
                         alt="" className="topAvatar2" />
                </div>
            </div>
        </div>
    );
}