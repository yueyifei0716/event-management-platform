import React, { useEffect, useContext, useState } from 'react';
import Topbar from "../../components/TopBar/UserTopBar";
import instance from '../../utils/axios';
import { Link } from 'react-router-dom';
import AuthContext from "../../context/AuthContext";
import Button from '@material-ui/core/Button';
import { extractUserId } from "../../utils/Token";
import Sidebar from "../../components/SideBar/UserSideBar";
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import './UserDetail.css';


const UserDetail = () => {

    // initialize the defaut state
    const [detail, setDetail] = useState({
        email: "",
        first_name: "",
        last_name: "",
        address: "",
        bill_method: "",
        account: "",
    });
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const params = {
        user_id: user_id,
        token: token,
    }

    // fetch all user detail
    useEffect(() => {
        fetchData();
    }, []);
    const fetchData = async () => {
        const result = await instance.get("user/detail", { params });
        setDetail(result.data);
    };

    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <Timeline>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Email:  {detail.email}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>First Name:  {detail.first_name}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Last Name:  {detail.last_name}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Address:  {detail.address}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Bill Method:  {detail.bill_method}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Account:  {detail.account}</TimelineContent>
                        </TimelineItem>
                        <TimelineItem sx={{ minHeight: '45px' }}>
                            <TimelineSeparator>
                                <TimelineDot />
                            </TimelineSeparator>
                            <TimelineContent sx={{ color: 'text.primary' }}>Balance:  {'$' + detail.balance}</TimelineContent>
                        </TimelineItem>
                    </Timeline>
                    <div className='btns'>
                        <Link style={{ textDecorationLine: 'none' }} to="/user_dashboard">
                            <Button id="shadowbtn" variant="contained" size='large' color="primary" >Back to home page</Button>
                        </Link>
                        <Link style={{ textDecorationLine: 'none', margin: '0 35px' }} to="/user_update_detail">
                            <Button id="shadowbtn" variant="contained" size='large' color="primary" >Edit Detail</Button>
                        </Link>
                        <Link style={{ textDecorationLine: 'none' }} to="/user_edit_account">
                            <Button id="shadowbtn" variant="contained" size='large' color="primary" >Edit Account</Button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default UserDetail