import "./sidebar.css";
import {
    LineStyle,
    Timeline,
    Storefront,
    BarChart,
} from "@material-ui/icons";
import { Link } from "react-router-dom";
import React from "react";


// the user side bar
export default function Sidebar() {
    return (
        <div className="sidebar">
            <div className="sidebarWrapper">
                <div className="sidebarMenu">
                    <h3 className="sidebarTitle">Dashboard</h3>
                    <ul className="sidebarList">
                        <Link to="/user_dashboard" className="link">
                            <li className="sidebarListItem active">
                                <LineStyle className="sidebarIcon" />
                                Home
                            </li>
                        </Link>
                        <Link to="/user_detail" className="link">
                            <li className="sidebarListItem">
                                <Storefront className="sidebarIcon" />
                                My Detail
                            </li>
                        </Link>
                        <Link to="/user_reset" className="link">
                            <li className="sidebarListItem">
                                <Timeline className="sidebarIcon" />
                                Reset Password
                            </li>
                        </Link>
                    </ul>
                </div>
                <div className="sidebarMenu">
                    <h3 className="sidebarTitle">Quick Menu</h3>
                    <ul className="sidebarList">
                        <Link to="/user_addbalance" className="link">
                            <li className="sidebarListItem">
                                <Storefront className="sidebarIcon" />
                                Add Balance
                            </li>
                        </Link>

                        <Link to="/user_activity_list" className="link">
                            <li className="sidebarListItem">
                                <BarChart className="sidebarIcon" />
                                Your Activities
                            </li>
                        </Link>
                        <Link to="/act_user_like" className="link">
                            <li className="sidebarListItem">
                                <BarChart className="sidebarIcon" />
                                Maybe You Like
                            </li>
                        </Link>

                    </ul>
                </div>
            </div>
        </div>
    );
}