import {
    faBed,
    faCalendarDays,
    faPerson,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./header.css";
import React from 'react'
import { DateRange } from "react-date-range";
import { useContext, useState } from "react";
import "react-date-range/dist/styles.css"; // main css file
import "react-date-range/dist/theme/default.css"; // theme css file
import { format } from "date-fns";


const Header = () => {

    const [openDate, setOpenDate] = useState(false);
    const [dates, setDates] = useState([
        {
            startDate: new Date(),
            endDate: new Date(),
            key: "selection",
        },
    ]);
    return (
        <div className="header">
            <div className="headerContainer">

                <button className="headerBtn">Buy Ticket</button>
                <button className="headerBtn">More Details</button>
                <div className="headerSearch">
                    <div className="headerSearchItem">
                        <FontAwesomeIcon icon={faBed} className="headerIcon" />
                        <input
                            type="text"
                            placeholder="Your Favorite Activity"
                            className="headerSearchInput"
                        />
                    </div>
                    <div className="headerSearchItem">
                        <FontAwesomeIcon icon={faBed} className="headerIcon" />
                        <input
                            type="text"
                            placeholder="Description"
                            className="headerSearchInput"
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
                                minDate={new Date()}
                            />
                        )}
                    </div>
                    <div className="headerSearchItem">
                        <FontAwesomeIcon icon={faPerson} className="headerIcon" />
                        <span className="headerSearchText">Activity Type</span>
                        <select>
                            <option>music</option>
                            <option>magical</option>
                        </select>
                    </div>
                    <div className="headerSearchItem">
                        <button className="headerBtn">
                            Search
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}


export default Header