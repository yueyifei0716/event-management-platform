import "./newactivity.css";
import instance from "../../utils/axios";
import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Topbar from "../../components/TopBar/TopBar";
import Sidebar from "../../components/SideBar/SideBar";
import FormInput from "../../components/FormInput/FormInput";
import Grid from '@mui/material/Grid';
import AuthContext from "../../context/AuthContext";
import { extractHostId } from "../../utils/Token";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


const NewActivity = () => {

    // initialize the defaut state
    const [values, setValues] = useState({
        name: "",
        description: "",
        type: "",
        venue_name: "",
        venue_address: "",
        start_date: "",
        end_date: "",
        all_ticket: "",
        possible_seats: "",
        ticket_money: "",
        seat_x: "",
        seat_y: "",
        image: "",
    });
    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();
    const { token } = useContext(AuthContext);
    const host_id = extractHostId(token);
    const data = {
        host_id: parseInt(host_id),
        activity: values,
        token: token
    }

    // define the parameters of the input boxes in the form
    const inputs = [
        {
            id: 1,
            name: "name",
            type: "text",
            placeholder: "Activity Name",
            errorMessage: "The activity name is empty!",
            label: "Activity Name",
            required: true,
        },
        {
            id: 2,
            name: "description",
            type: "text",
            placeholder: "Description",
            errorMessage: "The description is empty!",
            label: "Description",
            required: true,
        },
        {
            id: 3,
            name: "type",
            type: "text",
            placeholder: "Activity Type",
            label: "Activity Type",
            required: true,
        },
        {
            id: 4,
            name: "venue_name",
            type: "text",
            placeholder: "Venue Name",
            errorMessage: "The venue name is empty!",
            label: "Venue Name",
            required: true,
        },
        {
            id: 5,
            name: "venue_address",
            type: "text",
            placeholder: "Venue Address",
            errorMessage: "The venue address is empty!",
            label: "Venue Address",
            required: true,
        },
        {
            id: 6,
            name: "start_date",
            type: "datetime-local",
            placeholder: "Start Time",
            label: "Start Time",
            required: true,
        },
        {
            id: 7,
            name: "end_date",
            type: "datetime-local",
            placeholder: "End Time",
            label: "End Time",
            required: true,
        },
        {
            id: 8,
            name: "all_ticket",
            type: "number",
            placeholder: "All Tickets",
            errorMessage: "The tickets number is empty!",
            label: "All Tickets",
            required: true,
        },
        {
            id: 9,
            name: "possible_seats",
            type: "number",
            placeholder: "Possible Seats",
            errorMessage: "The seats number is empty!",
            label: "Possible Seats",
            required: true,
        },
        {
            id: 10,
            name: "ticket_money",
            type: "number",
            placeholder: "Ticket Money",
            errorMessage: "The ticket money is empty!",
            label: "Ticket Money",
            required: true,
        },
        {
            id: 11,
            name: "seat_x",
            type: "number",
            placeholder: "Row",
            errorMessage: "The row is empty!",
            label: "Row",
            required: true,
        },
        {
            id: 12,
            name: "seat_y",
            type: "number",
            placeholder: "Column",
            errorMessage: "The column is empty!",
            label: "Column",
            required: true,
        },
        {
            id: 13,
            name: "image",
            type: "text",
            placeholder: "Paste image link",
            errorMessage: "The image is empty!",
            label: "Image",
            required: true,
        },
    ];

    // handle onChange action for each input box
    const handleChange = (e) => {
        setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleChange2 = (event) => {
        setValues({ ...values, type: event.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await instance.post("/host/newactivity", data);
            navigate("/host_dashboard");
            setError(false);
            setSuccess(true);
        } catch (err) {
            setError(true);
            setSuccess(false);
        }
    };


    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div className="formContainer5">
                        <div className="formWrapper5">
                            <span className="newActTitle"> Create New Activity </span>
                            <form onSubmit={handleSubmit}>
                                <Grid container spacing={1}>
                                    {inputs.map((input) => {
                                        if (input.id === 3) {
                                            return (
                                                <Grid item xs={6}>
                                                    <FormControl sx={{ width: 280 }}>
                                                        <InputLabel id="demo-simple-select-label"> {values.type || 'Activity Type'} </InputLabel>
                                                        <Select
                                                            labelId="demo-simple-select-label"
                                                            id="demo-simple-select"
                                                            value={values.type}
                                                            label="Activity Type"
                                                            onChange={handleChange2}
                                                        >
                                                            <MenuItem value='magical'> Magical</MenuItem>
                                                            <MenuItem value='music'> Music </MenuItem>
                                                        </Select>
                                                    </FormControl>
                                                </Grid>
                                            )
                                        } else {
                                            return (
                                                <Grid item xs={6}>
                                                    <FormInput
                                                        key={input.id}
                                                        {...input}
                                                        onChange={handleChange}
                                                    />
                                                </Grid>
                                            )
                                        }
                                    })}
                                    <span className="title2">If your image src url is invalid, then the default image will be used.</span>
                                    <img className="pic" src={values.image} onError={(e) => {
                                        e.target.src = 'data:image/jpeg;base64,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' // some replacement image
                                        e.target.style = 'padding: 8px; margin: 16px' // inline styles in html format
                                        setValues((prev) => ({ ...prev, ['image']: e.target.src }));
                                    }} alt="" />

                                </Grid>
                                <button className="submit" type='submit'> Submit </button>
                            </form>
                            <Link to="/">
                                <button className="home">Back to home page</button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default NewActivity