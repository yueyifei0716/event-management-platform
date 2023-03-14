import React, { useState, useContext, useEffect } from 'react';
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";
import instance from '../../utils/axios';
import { Link, useLocation } from 'react-router-dom';


const UserDetailPublic = () => {

    // initialize the defaut state
    const location = useLocation();
    const { user_detail_public } = location.state;
    const [detail, setDetail] = useState({
        email: "",
        first_name: "",
        last_name: "",
        address:"",

    });
    const params = {
        user_id: user_detail_public,
    };

    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/user/detail/public", { params });
            return result.data
        };
        fetchData().then(data => setDetail(data));
    }, []);

    return (
        <div className="home">
            <Topbar />

                <div className="others">
                <div>email:  { detail.email }</div>
                <div>first_name:  { detail.first_name }</div>
                <div>last_name:  { detail.last_name }</div>
                <div>address:  { detail.address }</div>
                </div>
                <Link to="/">
                    <button className="home">Back to</button>
                </Link>
        </div>

    )
}

export default UserDetailPublic