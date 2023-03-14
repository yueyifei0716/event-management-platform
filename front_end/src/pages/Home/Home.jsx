import React, { useEffect, useState } from 'react'
import Navbar from "../../components/NavBar/NavBar";
import Header from "../../components/Header/Header";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBed, faCalendarDays, faPlane } from "@fortawesome/free-solid-svg-icons";
import { format } from "date-fns";
import { DateRange } from "react-date-range";
import instance from '../../utils/axios';
import { Link } from "react-router-dom";
import SnowStorm from 'react-snowstorm';
import "./home.css";
import "../../components/Effects/square.css"


const footData = [
    {
        title: 'Support',
        list: ['Mysql', 'Python', 'React', 'flask']
    },
    {
        title: 'Connect',
        list: ['Comp3900sender1@163.com', '', '', '']
    },
    {
        title: 'Maker',
        list: ['SHI MINXIN', 'CHANG RUIHE', 'JIA FENGBO', 'YUE YIFEI']
    },
    {
        title: 'About',
        list: ['2022 - Event Management', 'Cookies Settings', 'Cookies and Privacy', 'Terms of Use']
    },
]


const Home = () => {

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

    const handleSearchChange = (e) => {
        setType(e.target.value);
    };

    // search and fetch all activities by the activity name, description, type and time
    const submitSearch = () => {
        const result = instance.get("/activities/search", { params }).then((res) => {
            return res.data
        });
        result.then((data) => {
            let start_date = dates[0].startDate.toISOString().substring(0, 10)
            let end_date = dates[0].endDate.toISOString().substring(0, 10)
            let newActs = data.filter((act) => (act.start_date >= start_date && act.end_date <= end_date))
            setTimeout(() => {
                setActivities(newActs)
            }, 0);
        });
    };

    // fetch all activities in the next month and diaplay by default
    useEffect(() => {
        const fetchData = async () => {
            const result = await instance.get("/activities/listallavaiable");
            return result.data
        };
        fetchData().then(data => setActivities(data));
    }, []);

    // the button action handling the clear of date
    const handleClearDate = async (e) => {
        e.preventDefault();
        await instance.delete("/clear/v1");
    };

    // the button action handling the clear of token
    const handleClearToken = async (e) => {
        e.preventDefault();
        await instance.get("/clear/token");
        localStorage.removeItem("token");
        localStorage.removeItem("user_id");
        localStorage.removeItem("host_id");
    };

    return (
        <div>
            <SnowStorm />
            <Navbar />
            {/* display the information about the system in header */}
            <div className="header1">
                <div class="square">
                    <ul class="square-ul">
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                    </ul>
                </div>
                <div class="circle">
                    <ul>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                    </ul>
                </div>
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
                        The buttons below are shortcut buttons to better display the system in a limited time. <br />
                    </p>
                    <Link to="/time_set">
                        <button className="topheaderBtn" id="shadowbtn"> Set Now Time </button>
                    </Link>
                    <Link to="/time_push">
                        <button className="topheaderBtn" id="shadowbtn"> Push Now Time </button>
                    </Link>
                    <Link to="/all_infor">
                        <button className="topheaderBtn" id="shadowbtn"> All Information </button>
                    </Link>
                    <button className="topheaderBtn" id="shadowbtn" onClick={handleClearDate}>
                        Clear Data
                    </button>
                    <button className="topheaderBtn" id="shadowbtn" onClick={handleClearToken}>
                        Clear Token
                    </button>

                    {/* display the search bar */}
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
                                />
                            )}
                        </div>
                        <div className="headerSearchItem">
                            <FontAwesomeIcon icon={faBed} className="headerIcon" />
                            <span className="headerSearchText">Activity Type</span>
                            <select onChange={handleSearchChange}>
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
            {/* display all activities with image, title and date by iteration */}
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
            {/* display the information about the authurs */}
            <div className='foot'>
                <div className='content'>
                    {footData.map((v, i) => {
                        return (
                            <div className='outList' key={i}>
                                <div className='title'>{v.title}</div>
                                {v.list.map((val, index) => {
                                    return <div className='list-item' key={index}>{val}</div>
                                })}
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}

export default Home