import React, { useState, useContext, useEffect } from 'react';
import instance from '../../utils/axios';
import { Link } from "react-router-dom";
import { DataGrid } from '@mui/x-data-grid';
import AuthContext from "../../context/AuthContext";
import { extractHostId } from "../../utils/Token";
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";
import MyModal from '../../components/Confirmation/Confirmation';
import "./hostactivitylist.css";


const HostActivityList = () => {

    // initialize the defaut state
    const [open, setOpen] = useState(false);
    const [activity_id, setactivity_id] = useState('');
    const [myActivities, setMyActivities] = useState([]);

    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);
    const params = {
        host_id: parseInt(host_id),
        token: token
    }

    const handleClose = async (newValue) => {
        setOpen(false);
        if (newValue) {
            // confirmation window
            instance.post('host/cancelactivity',
                { activity_id: activity_id, host_id: host_id, token: token }).
                then(res => {
                    {
                        setOpen(false);
                        window.location.reload();
                    }
                }).catch(err => {
                    console.log(err);
                });
            console.log('check');
        }
    };

    const handleCancel = async (activity_id) => {
        setOpen(true);
        setactivity_id(activity_id)
    }

    // fetch all activities created by the host
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("host/listactivities", { params });
            return result.data
        };
        fetchData().then(data => setMyActivities(data["activities_info"]));
    }, []);

    // define the data table
    const columns = [
        { field: 'id', headerName: 'ID', width: 20, headerAlign: 'center' },
        { field: 'name', headerName: 'Name', width: 110, headerAlign: 'center' },
        { field: 'type', headerName: 'Type', width: 80, headerAlign: 'center' },
        { field: 'start_date', headerName: 'Start Date', width: 100, headerAlign: 'center' },
        { field: 'end_date', headerName: 'End Date', width: 100, headerAlign: 'center' },
        { field: 'possible_seats', headerName: 'Possible Seats', type: 'number', width: 120, headerAlign: 'center',align: "center" },
        { field: 'ticket_money', headerName: 'Ticket Money', width: 100, headerAlign: 'center', align: "center" },
        {
            field: "action",
            headerName: "Action",
            width: 280,
            headerAlign: 'center',
            renderCell: (params) => {
                return (
                    <>
                        <Link to={"/host_broadcast"}
                            state={{ activity_id: params.row.act_id }}
                        >
                            <button className="productListEdit">Broadcast</button>
                        </Link>
                        <Link to={`/activity_detail/${params.row.act_id}`}
                            state={{ activity_detail: myActivities.find(item => item.id === params.row.act_id) }}
                        >
                            <button className="productListEdit">Details</button>
                        </Link>
                        <button className="productListEdit" onClick={() => handleCancel(params.row.act_id)}>Cancel</button>
                    </>
                );
            },
        },
    ];

    const rows = myActivities.map(({ id, act_id, name, type, start_date, end_date, possible_seats, ticket_money }) =>
        ({ id, act_id, name, type, start_date, end_date, possible_seats, ticket_money: ticket_money }));

    return (
        <div className="home" id='hostactivitylist'>
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
                        />
                    </div>
                </div>
            </div>
            <MyModal
                open={open}
                onClose={handleClose}
                title="Cancel Activity"
                content="Are you sure to cancel this activity?"
            />
        </div>
    )
}

export default HostActivityList