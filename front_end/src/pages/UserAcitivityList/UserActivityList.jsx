import React, { useState, useContext, useEffect } from 'react';
import instance from '../../utils/axios';
import { Link } from "react-router-dom";
import { DataGrid } from '@mui/x-data-grid';
import AuthContext from "../../context/AuthContext";
import { extractUserId } from "../../utils/Token";
import Topbar from "../../components/TopBar/UserTopBar";
import Sidebar from "../../components/SideBar/UserSideBar";
import MyModal from '../../components/Confirmation/Confirmation';


const UserActivityList = () => {

    // initialize the defaut state
    const [open, setOpen] = useState(false);
    const [rowObj, setrowObj] = useState({
        activity_id: '',
        host_id: '',
        token: '',
        booking_id: '',
    });
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const params = {
        user_id: parseInt(user_id),
        token: token
    }
    const [myActivities, setMyActivities] = useState([]);

    const handleClose = async (newValue) => {
        setOpen(false);
        if (newValue) {
            // confirmation window
            instance.post('/user/cancel', { activity_id: rowObj.activity_id, booking_id: rowObj.booking_id, user_id: user_id, token: token }).then(res => {
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

    // fetch all activities created by the host
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/user/listactivities", { params });
            return result.data;
        };
        fetchData().then(data => setMyActivities(data["activities_info"]));
    }, []);

    const handleCancel = async (act_id, booking_id, user_id, token) => {
        setOpen(true);
        setrowObj({ activity_id: act_id, booking_id: booking_id, user_id: user_id, token: token });
    }

    // define the data table
    const columns = [
        { field: 'id', headerName: 'Booking ID', width: 85, headerAlign: 'center' },
        { field: 'act_id', headerName: 'Act ID', width: 60, hide: true, headerAlign: 'center' },
        { field: 'name', headerName: 'Activity Name', width: 110, headerAlign: 'center' },
        { field: 'hold_host', headerName: 'Host Hold', width: 10, hide: true, headerAlign: 'center' },
        {
            field: 'host_name',
            headerName: 'Host Name',
            width: 160,
            headerAlign: 'center',
            renderCell: (params) => {
                return (
                    <>
                        <Link to={"/user_book_host/"}
                            // 在这里user登录去看host的detail并且可以book
                            state={{
                                host_id: params.row.hold_host,
                                host_name: params.row.host_name
                            }}
                        >
                            {params.row.host_name}
                        </Link>
                    </>
                )
            }
        },
        { field: 'type', headerName: 'Type', width: 70, headerAlign: 'center' },
        { field: 'start_date', headerName: 'Start Date', width: 100, headerAlign: 'center' },
        { field: 'end_date', headerName: 'End Date', width: 100, headerAlign: 'center' },
        { field: 'seat_x', headerName: 'Seat x', type: 'number', width: 60, headerAlign: 'center' },
        { field: 'seat_y', headerName: 'Seat y', type: 'number', width: 60, headerAlign: 'center' },
        { field: 'ticket_money', headerName: 'Ticket Money', width: 100, headerAlign: 'center', align: "center" },
        {
            field: "action",
            headerName: "Action",
            headerAlign: 'center',
            width: 180,
            renderCell: (params) => {
                return (
                    <>
                        <Link to={`/activity_detail/${params.row.act_id}`}
                        >
                            <button className="productListEdit">Details</button>
                        </Link>
                        <button className="productListEdit" onClick={() => handleCancel(params.row.act_id, params.row.booking_id, user_id, token)}>Cancel</button>
                    </>
                );
            },
        },
    ];

    const rows = myActivities.map(({ id, booking_id, act_id, name, hold_host, host_name, type, start_date, end_date, seat_x, seat_y, ticket_money }) =>
        ({ id, booking_id, act_id, name, hold_host, host_name, type, start_date, end_date, seat_x, seat_y, ticket_money }));

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
                            getRowId={row => row.booking_id}
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

export default UserActivityList