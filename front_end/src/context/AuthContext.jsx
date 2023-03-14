import React from 'react';
import { createContext, useState } from 'react';

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(
        localStorage.getItem("token")
    );

    // set the user or host auth detail and save all the information to the localStorage
    const setAuthDetail = (token, user_id, host_id) => {
        localStorage.setItem("token", token);
        localStorage.setItem("user_id", user_id);
        localStorage.setItem("host_id", host_id);
        setToken(token);
    }

    // provide auth context to all of the pages
    return (
        <AuthContext.Provider value={{ token, setAuthDetail }}>
            { children }
        </AuthContext.Provider>
    )
}

export default AuthContext;