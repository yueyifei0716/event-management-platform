import React from 'react';
import ReactRain from 'react-rain-animation';

// import all the styles
import "react-rain-animation/lib/style.css";


const Rain = (props) => {

    return (
        <ReactRain
            numDrops="500"
        />
    )

}

export default Rain;