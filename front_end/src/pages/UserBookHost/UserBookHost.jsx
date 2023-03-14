import React, { useState, useContext, useEffect } from 'react';
import Topbar from "../../components/TopBar/UserTopBar";
import Sidebar from "../../components/SideBar/UserSideBar";
import instance from '../../utils/axios';
import { Link, useLocation } from 'react-router-dom';
import AuthContext from "../../context/AuthContext";
import { extractUserId } from "../../utils/Token";
import { DataGrid } from "@mui/x-data-grid";
import Button from "@mui/material/Button";
import { encodeId } from "../../utils/CodingId";


const HostDetail = () => {

    // initialize the defaut state
    const [booked, setBooked] = useState(false);
    const [myActivities, setMyActivities] = useState([]);
    const location = useLocation();
    const { host_id, host_name } = location.state;
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const params = {
        host_id: encodeId(host_id),
        user_id: parseInt(user_id),
        token: token,
    }

    // fetch all host detail and display
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/host/detail", { params });
            return result.data;
        };
        fetchData()
            .then(data => {
                setBooked(data['is_booked']);
                setMyActivities(data['list_of_act']);
            })
    }, []);

    // the button action handling the subscription of host
    const handleBook = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/user/bookhost", params);
            setBooked(!booked);
        } catch (err) {}
    };

    const columns = [
        { field: 'id', headerName: 'ID', width: 20, headerAlign: 'center' },
        { field: 'name', headerName: 'Name', width: 110, headerAlign: 'center' },
        { field: 'type', headerName: 'Type', width: 80, headerAlign: 'center' },
        { field: 'start_date', headerName: 'Start Date', width: 100, headerAlign: 'center' },
        { field: 'end_date', headerName: 'End Date', width: 100, headerAlign: 'center' },
        { field: 'possible_seats', headerName: 'Possible Seats', type: 'number', width: 150, headerAlign: 'left', align: "center" },
        { field: 'ticket_money', headerName: 'Ticket Money', width: 120, headerAlign: 'right', align: "center" },
        {
            field: "action",
            headerName: "Action",
            headerAlign: 'center',
            width: 100,
            renderCell: (params) => {
                return (
                    <>
                        <Link to={`/activity_detail/${params.row.act_id}`}
                            state={{ activity_detail: myActivities.find(item => item.id === params.row.act_id) }}
                        >
                            <button className="productListEdit">Details</button>
                        </Link>
                    </>
                );
            },
        },
    ];

    const rows = myActivities.map(({ id, act_id, name, type, start_date, end_date, possible_seats, ticket_money }) =>
        ({ id, act_id, name, type, start_date, end_date, possible_seats, ticket_money }));

    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div className='title'> The email of the host: {host_name} </div>
                    <br />
                    <div className='title'> The total amount of activities: {myActivities.length} </div>
                    <br />
                    <Button variant="contained" onClick={handleBook}>{booked ? "Unsubscribe" : "Subscribe"}</Button>
                    <br />
                    <br />
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
        </div>
    )
}

export default HostDetail