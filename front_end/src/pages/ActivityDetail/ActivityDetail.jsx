import React, { useContext, useEffect, useState } from 'react';
import { Link, useParams, useNavigate } from "react-router-dom";
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import instance from '../../utils/axios';
import AuthContext from "../../context/AuthContext";
import { extractUserId, extractHostId } from "../../utils/Token";
import Comments from "../../components/Comments/Comments";
import MyModal from '../../components/Confirmation/Confirmation';
import { DataGrid } from '@mui/x-data-grid';
import "./activitydetail.css"


const ActivityDetail = () => {

    const columns = [
        { field: 'id', headerName: 'Number ID', width: 110 },
        { field: 'seat_x', headerName: 'seat x', width: 60 },
        { field: 'seat_y', headerName: 'seat y', width: 110 }
    ]

    // initialize the defaut state
    const [open, setOpen] = useState(false);
    const [rows, setrows] = useState([]);
    const [seeopen, setseeOpen] = useState(false);
    const act_id = parseInt(useParams().act_id);
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const host_id = extractHostId(token);
    const params = { a_id: act_id };
    const [activityDetail, setActivityDetail] = useState({});
    const [values, setValues] = useState({
        activity_id: act_id,
        user_id: parseInt(user_id),
        seat_x: 0,
        seat_y: 0,
        token: token,
    });
    const theme = createTheme();
    const navigate = useNavigate();

    // fetch the activity in the next month and diaplay by default
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/user/activities/list", { params });
            return result.data
        };
        fetchData().then(data => setActivityDetail(data));
    }, []);

    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleClose = async (newValue) => {
        setOpen(false);
        if (newValue) {
            // 确认
            try {
                await instance.post("/user/activitybook", values);
                navigate("/user_dashboard");

            } catch (err) {

            }
            console.log('check');
        }

    };

    const handleSeeClose = async (newValue) => {
        setseeOpen(false);
        if (newValue) {
            // 确认
            console.log('check');
        }
    };

    const handleBuy = async (e) => {
        e.preventDefault();
        setOpen(true);
    };

    const handleSee = async (e) => {
        e.preventDefault();
        setseeOpen(true);
        instance.get("/act/seat", { params: { act_id: act_id } }).then((res) => {
            setrows(res.data || []);
        })
    };

    // get the notification and image url link of the activity
    const notification = activityDetail.notification || '';
    const image_url = activityDetail.image || '';

    return (
        <div className="home">
            <div className="container">
                <ThemeProvider theme={theme}>
                    <Grid container component="main" sx={{ background: 'linear-gradient(200deg,#a8edea,#fed6e3)' }}>
                        <CssBaseline />
                        {/* display the cover image of the activity on the left hand side */}
                        <Grid
                            item xs={false} sm={4} md={7}
                            sx={{
                                backgroundImage: `url(${image_url})`,
                                backgroundRepeat: 'no-repeat',
                                borderRadius: '10px',
                                backgroundSize: 'contain',
                                backgroundPosition: 'center',
                            }}
                        />
                        {/* display the all the detailed information about the activity on the right hand side */}
                        <Grid
                            item xs={12} sm={8} md={5} component={Paper} elevation={6} square
                            sx={{ borderRadius: '10px' }}
                        >
                            {/* show all the detailed information about the activity in a box */}
                            <Box
                                sx={{
                                    my: 8,
                                    mx: 4,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                }}
                            >
                                <Typography component="h1" variant="h5">
                                    Activity Details
                                </Typography>
                                <br />
                                <br />
                                { user_id ? (
                                    <Typography variant="body1" style={{ width: '80%' }} component={'span'} display="block" gutterBottom>
                                        <div className='text-left'>Host name:</div>
                                        <Link to={"/user_book_host/"}
                                            className="text-right"
                                            state={{
                                                host_id: activityDetail.hold_host,
                                                host_name: activityDetail.host_name
                                            }}
                                        >
                                            { activityDetail.host_name }
                                        </Link>
                                    </Typography>
                                ) : (
                                    <Typography variant="body1" style={{ width: '80%' }} component={'span'} display="block" gutterBottom>
                                        <div className='text-left'>Host name:</div> <span className='text-right'>{activityDetail.host_name}</span>
                                    </Typography>
                                )}
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} align='left' display="block" gutterBottom>
                                    <div className='text-left'>Activity name:</div>  <span className='text-right'>{activityDetail.name}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} align='left' display="block" gutterBottom>
                                    <div className='text-left'>Description:</div>  <span className='text-right'>{activityDetail.description}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Type:</div>  <span className='text-right'>{activityDetail.type}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Venue name:</div>  <span className='text-right'>{activityDetail.venue_name}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Venue address:</div>  <span className='text-right'>{activityDetail.venue_address}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Start date:</div>  <span className='text-right'>{activityDetail.start_date}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Start time:</div>  <span className='text-right'>{activityDetail.start_time}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>End date:</div>  <span className='text-right'>{activityDetail.end_date}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>End time:</div>  <span className='text-right'>{activityDetail.end_time}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>All ticket:</div>  <span className='text-right'>{activityDetail.all_ticket}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Possible seats:</div>  <span className='text-right'>{activityDetail.possible_seats}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Ticket money:</div>  <span className='text-right'>{'$' + activityDetail.ticket_money}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Seat x:</div>  <span className='text-right'>{activityDetail.seat_x}</span>
                                </Typography>
                                <Typography variant="body1" component={'span'} style={{ width: '80%' }} display="block" gutterBottom>
                                    <div className='text-left'>Seat y:</div>  <span className='text-right'>{activityDetail.seat_y}</span>
                                </Typography>
                                { notification ? notification.map((item) => {
                                    return (
                                        <Typography style={{ width: '80%' }} variant="body1" component={'span'} display="block" gutterBottom key={item.id}>
                                            <div className='text-left'>Notification:</div>  <span className='text-right'>{item.id}: {item.message}</span>
                                        </Typography>
                                    )
                                }) : <div></div> }
                            </Box>
                            { user_id ? (
                                <Box textAlign='center'>
                                    <TextField
                                        required
                                        id="outlined-required"
                                        label="Row"
                                        value={values["seat_x"]}
                                        name="seat_x"
                                        onChange={handleChange}
                                    />
                                    <br />
                                    <br />
                                    <TextField
                                        required
                                        id="outlined-required"
                                        label="Column"
                                        value={values["seat_y"]}
                                        name="seat_y"
                                        onChange={handleChange}
                                    />
                                    <br />
                                    <br />
                                    <Button variant='contained' id="shadowbtn" size='medium' onClick={handleBuy}>
                                        Buy Tickets
                                    </Button>
                                    <Button variant='contained' id="shadowbtn" size='medium' color='success' style={{ marginLeft: '15px' }} onClick={handleSee}>
                                        See Booking Seat
                                    </Button>
                                    <br />
                                    <Divider />
                                </Box>
                            ) : null }

                            {/* show the comments */}
                            <Comments a_id={act_id} />
                            <Box sx={{ '& button': { m: 1 } }} textAlign='center'>
                                {user_id ? (
                                    <Link to="/user_activity_list">
                                        <Button variant="contained" size="small">Back</Button>
                                    </Link>
                                ) : host_id ? (
                                    <Link to="/host_activity_list">
                                        <Button variant="contained" size="small">Back</Button>
                                    </Link>
                                ) : (
                                    <Link to="/">
                                        <Button variant="contained" size="small">Back</Button>
                                    </Link>
                                )}
                            </Box>
                        </Grid>
                    </Grid>
                </ThemeProvider>
            </div>
            <MyModal
                open={open}
                onClose={handleClose}
                title="Buy Activity"
                content="Are you sure to Buy this activity?"
            />
            <MyModal
                open={seeopen}
                onClose={handleSeeClose}
                title="See Booking Seat"
                contentStyle={{ height: '600px' }}
                isBackBtn={false}
            >
                <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSize={5}
                    rowsPerPageOptions={[5]}
                />

            </MyModal>
        </div>
    )
}

export default ActivityDetail