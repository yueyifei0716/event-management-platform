import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import Topbar from "../../components/TopBar/UserTopBar";
import Sidebar from "../../components/SideBar/UserSideBar";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBed, faCalendarDays, faPlane } from "@fortawesome/free-solid-svg-icons";
import { format } from "date-fns";
import { DateRange } from "react-date-range";
import "./userdashboard.css";
import instance from '../../utils/axios';


const UserDashBoard = () => {

    // initialize the defaut state
    const [name, setName] = useState("");
    const [type, setType] = useState("music");
    const [description, setdescription] = useState("");
    const [openDate, setOpenDate] = useState(false);
    const [dates, setDates] = useState([
        {
            startDate: new Date(2018, 0, 1),
            endDate: new Date(2023, 0, 1),
            key: "selection",
        },
    ]);
    const [activities, setActivities] = useState([]);
    const params = {
        name: name,
        description: description,
        type: type,
    }

    // search and fetch all activities by the activity name, description, type and time
    const submitSearch = () => {
        const result = instance.get("/activities/search", { params }).then((res) => {
            return res.data;
        });
        result.then((data) => {
            let start_date = dates[0].startDate.toISOString().substring(0, 10);
            let end_date = dates[0].endDate.toISOString().substring(0, 10);
            let newActs = data.filter((act) => (act.start_date >= start_date && act.end_date <= end_date));
            setActivities(newActs);
        });
    };

    // handle onChange action for each input box
    const handleChange2 = (e) => {
        setType(e.target.value);
    };

    // fetch all activities in the next month and diaplay by default
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/activities/listallavaiable");
            return result.data;
        };
        fetchData().then(data => setActivities(data));
    }, []);


    return (
        <div className="home">
            <Topbar />
            <div className="container">
                <Sidebar />
                <div className="others">
                    <div className="header1">
                        <div className="headerContainer">
                            <div className="headerList">
                                <div className="headerListItem">
                                    <FontAwesomeIcon className="headerIcon" icon={faPlane} size="2x" />
                                    <span className="headerListItemText"> System Home Page </span>
                                </div>
                            </div>
                            <h1 className="headerTitle">
                                Event Booking Comment System
                            </h1>
                            <p className="headerDesc">
                                Welcome! <br />
                                The table below is about the activities valid for one month.<br />
                            </p>

                            <div className="headerSearch1">
                                <div className="headerSearchItem">
                                    <FontAwesomeIcon icon={faBed} className="headerIcon" />
                                    <input
                                        type="text"
                                        placeholder="Your Favorite Activity"
                                        className="headerSearchInput"
                                        onChange={(e) => setName(e.target.value)}
                                    />
                                </div>
                                <div className="headerSearchItem">
                                    <FontAwesomeIcon icon={faBed} className="headerIcon" />
                                    <input
                                        type="text"
                                        placeholder="Description"
                                        className="headerSearchInput"
                                        onChange={(e) => setdescription(e.target.value)}
                                    />
                                </div>
                                <div className="headerSearchItem">
                                    <FontAwesomeIcon icon={faCalendarDays} className="headerIcon" />
                                    <span
                                        onClick={() => setOpenDate(!openDate)}
                                        className="headerSearchText"
                                    >{`${format(dates[0].startDate, "MM/dd/yyyy")} to ${format(
                                        dates[0].endDate,
                                        "MM/dd/yyyy"
                                    )}`}
                                    </span>
                                    {openDate && (
                                        <DateRange
                                            editableDateInputs={true}
                                            onChange={(item) => setDates([item.selection])}
                                            moveRangeOnFirstSelection={false}
                                            ranges={dates}
                                            className="date"
                                        // minDate={new Date()}
                                        />
                                    )}
                                </div>
                                <div className="headerSearchItem">
                                    <FontAwesomeIcon icon={faBed} className="headerIcon" />
                                    <span className="headerSearchText">Activity Type</span>
                                    <select onChange={handleChange2}>
                                        <option value="music">music</option>
                                        <option value="magical">magical</option>
                                    </select>
                                </div>
                                <div className="headerSearchItem">
                                    <button className="headerBtn" onClick={submitSearch}>
                                        Search
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="homeContainer">
                        <div className="featured">
                            {activities.length !== 0 && activities[0] !== 'There is no activity recently' ? activities.map((act) => {
                                return (
                                    <div key={act.id} className="featuredItem">
                                        <Link to={`/activity_detail/${act.id}`} state={{ activity_detail: activities.find(item => item.id === act.id) }}>
                                            <img
                                                src={act.image}
                                                alt=""
                                                className="featuredImg"
                                            />
                                        </Link>
                                        <div className="featuredTitles">
                                            <h1>{act.name}</h1>
                                            <h2>From: {act.start_date}</h2>
                                            <h2>To: {act.end_date}</h2>
                                        </div>
                                    </div>
                                )
                            }) : <div></div>
                            }
                        </div>
                    </div>

                </div>
            </div>

        </div>
    )
}

export default UserDashBoard