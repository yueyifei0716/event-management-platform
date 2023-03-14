import "./navbar.css";
import React from 'react'
import { Link } from "react-router-dom";


// the navigate bar
const Navbar = () => {
    return (
        <div className="navbar">
            <div className="navContainer">
                <span className="logo">
                    <img src= {require('../../asserts/logo/logo.png')}
                         alt="" className="topAvatar" />
                         UNeverSleepWell
                </span>
                <div className="navItems">
                    <Link to="/user_login">
                        <button  className="navButton">User Login</button>
                    </Link>
                    <Link to="/host_login">
                        <button  className="navButton">Host Login</button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Navbar;