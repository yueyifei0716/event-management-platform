import React, { useState, useContext, useEffect } from 'react';
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";
import instance from '../../utils/axios';
import { DataGrid } from '@mui/x-data-grid';
import { Link } from 'react-router-dom';
import AuthContext from "../../context/AuthContext";
import { extractHostId } from "../../utils/Token";
import "./hostfan.css";


const HostFan = () => {

    // initialize the defaut state
    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);
    const [fans, setFans] = useState([]);
    const params = {
        host_id: host_id,
        token: token,
    };

    // fetch all fans information of the host
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/host/fan", { params });
            return result.data
        };
        fetchData().then(data => setFans(data));
    }, []);

    // define the data tble
    const columns = [
        { field: 'email', headerName: 'User Email', width: 150 },
        { field: 'first_name', headerName: 'First Name', width: 150 },
        { field: 'last_name', headerName: 'Last Name', width: 150 },
    ];

    const rows = fans.map(({ email, first_name, last_name }) =>
        ({ email, first_name, last_name }));

    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div style={{ height: 400, width: '100%' }}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            pageSize={5}
                            rowsPerPageOptions={[5]}
                            checkboxSelection
                            getRowId={row => row.email}
                        />
                    </div>
                    <Link to="/host_dashboard">
                        <button className="hostfan">Back to home page</button>
                    </Link>
                </div>
            </div>
        </div>
    )
}

export default HostFan