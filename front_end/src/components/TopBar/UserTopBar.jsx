import "./topbar.css";
import React, { useContext, useEffect, useState } from "react";
import { NotificationsNone } from "@material-ui/icons";
import { Link, useNavigate } from "react-router-dom";
import Noti from "../Drawer/Noti";
import instance from '../../utils/axios';
import { extractUserId } from "../../utils/Token";
import AuthContext from "../../context/AuthContext";


// the user top bar
export default function Topbar() {
    const navigate = useNavigate();
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const [isOpen, setisOpen] = useState(false)
    const [num, setnum] = useState(0)
    const [name, setName] = useState('')

    const handleLogout = async (e) => {
        e.preventDefault();
        await instance.post("/user/logout", { user_id, token });
        // after logout, remove the token and corresponding id in the localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("user_id");
        navigate("/");
    };

    // get the name of the host
    useEffect(() => {
        getName()
    }, [])

    const getName = () => {
        let params = {
            user_id: user_id,
        }
        instance.post("/user/name", params).then(res => {
            let name = res.data.name || []
            setName(name)
        })
    }


    const openFun = () => {
        setisOpen(true)
    }

    const changeNum = (v) => {
        setnum(v)
    }

    return (
        <div className="topbar">
            <Noti isOpen={isOpen} changeNum={changeNum}  closeFun={() => setisOpen(false)}/>
            <div className="topbarWrapper">
                <div className="topLeft">
                    <span className="logo">
                    <img src= {require('../../asserts/logo/logo.png')}
                         alt="" className="topAvatar" />
                         UNeverSleepWell
                    </span>
                </div>
                <div className="topRight">
                    <div className="topbarIconContainer">
                        <NotificationsNone onClick={openFun} name = 'notification-btn'/>

                        <span className="topIconBadge">{num}</span>
                    </div>

                    <Link to="/">
                        <button className="navButton" onClick={handleLogout}>Logout</button>
                    </Link>
                    <span className="email">{name}</span>
                    <img src= {require('../../asserts/logo/my.jpg')}
                         alt="" className="topAvatar2" />

                </div>
            </div>
        </div>
    );
}