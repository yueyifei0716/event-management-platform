import "./sidebar.css";
import {
    LineStyle,
    Timeline,
    PermIdentity,
    Storefront,
    BarChart,
} from "@material-ui/icons";
import { Link } from "react-router-dom";
import React from "react";

// the host side bar
export default function Sidebar() {
    return (
        <div className="sidebar">
            <div className="sidebarWrapper">
                <div className="sidebarMenu">
                    <h3 className="sidebarTitle">Dashboard</h3>
                    <ul className="sidebarList">
                        <Link to="/host_dashboard" className="link">
                            <li className="sidebarListItem active">
                                <LineStyle className="sidebarIcon" />
                                Home
                            </li>
                        </Link>
                        <Link to="/host_reset" className="link">
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
                        <Link to="/host_fan" className="link">
                            <li className="sidebarListItem">
                                <PermIdentity className="sidebarIcon" />
                                Your Fans
                            </li>
                        </Link>
                        <Link to="/new_activity" className="link">
                            <li className="sidebarListItem">
                                <Storefront className="sidebarIcon" />
                                New Activity
                            </li>
                        </Link>
                        <Link to="/host_activity_list" className="link">
                            <li className="sidebarListItem">
                                <BarChart className="sidebarIcon" />
                                Your Activities
                            </li>
                        </Link>
                    </ul>
                </div>
            </div>
        </div>
    );
}