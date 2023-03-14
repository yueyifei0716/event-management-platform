import { Outlet, Navigate } from 'react-router-dom'
import React, { useContext } from 'react';
import AuthContext from "../context/AuthContext";


// design a protection mechanisms for all routes except login,
// register, home page and other pages that don't need a valid token
const ProtectedRoute = () => {
    const { token } = useContext(AuthContext);
    // if the token is invalid, then navigate to the home page automaticlly
    return (
        token ? <Outlet /> : <Navigate to="/" />
    )
}

export default ProtectedRoute