import React,{useState,useEffect} from 'react'
import Rating from '@mui/material/Rating';

export default function MyRating(props) {
    const { defaultValue,onChangeRate,style,isdisabled=false } = props

    return (
        <div className='MyRating' style={style}>
            <Rating
                name="hover-feedback"
                value={defaultValue}
                precision={0.5}
                disabled={isdisabled}
                onChange={(event, newValue) => {
                    onChangeRate && onChangeRate(newValue)
                }}

            />
        </div>
    )
}