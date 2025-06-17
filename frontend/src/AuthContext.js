// frontend/src/AuthContext.js
import React, { createContext, useState, useContext, useMemo } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));

    const login = async (username, password) => {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to login');
        }
        const data = await response.json();
        setToken(data.access_token);
        localStorage.setItem('authToken', data.access_token);
    };

    const logout = () => {
        setToken(null);
        localStorage.removeItem('authToken');
    };

    // useMemo ensures this object is not recreated on every render
    const authContextValue = useMemo(() => ({
        token,
        login,
        logout
    }), [token]);

    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};