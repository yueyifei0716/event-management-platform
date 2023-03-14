import "./UserAddBalance.css";
import instance from '../../utils/axios';
import React, { useState, useContext } from "react";
import { makeStyles } from '@material-ui/core/styles';
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import { extractUserId } from "../../utils/Token";
import { Box, Button } from "@material-ui/core";
import Topbar from "../../components/TopBar/UserTopBar";
import Sidebar from "../../components/SideBar/UserSideBar";


// define the style of components
const useStyles = makeStyles((theme) => ({
    margin: {
        margin: theme.spacing(2),
        marginTop: 60,
        width: 100
    },
    extendedIcon: {
        marginRight: theme.spacing(1),
    },
}));

const UserAddBalance = () => {
    // initialize the defaut state
    const classes = useStyles();
    const [values, setValues] = useState({ money: 0 });
    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const params = {
        user_id: user_id,
        token: token,
        money: values.money,
    }
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/user/addbalance", params);
            navigate("/user_dashboard");
        } catch (err) {}
    };

    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div className="formContainer2">
                        <div className="formWrapper">
                            <div>
                                <div>
                                    <span className="title"> The recharge amount is: </span>
                                    <div className="num" style={{ textAlign: 'center' }}>{values.money}</div>
                                </div>
                                <Box>
                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 1 + prev.money }))
                                    }> + 1 </Button>

                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 5 + prev.money }))
                                    }> + 5 </Button>

                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 10 + prev.money }))
                                    }> + 10 </Button>
                                </Box>
                                <Box>
                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 20 + prev.money }))
                                    }> + 20 </Button>
                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 50 + prev.money }))
                                    }> + 50 </Button>

                                    <Button className={classes.margin} size="large" variant="contained" color="primary" onClick={() =>
                                        setValues((prev) => ({ ...prev, money: 100 + prev.money }))
                                    }> + 100 </Button>
                                </Box>
                            </div>
                            <br />
                            <div>
                                <form onSubmit={handleSubmit}>
                                    <button className="submit12" id="shadowbtn"> Submit </button>
                                </form>
                            </div>
                            <Link to="/user_dashboard">
                                <button className="home" id="shadowbtn" >Back to home page</button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default UserAddBalance