import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useAuth } from '../AuthContext'; 

const AdminRoute = ({ element, ...rest }) => {
    const { isAdmin } = useAuth();

    return (
        <Route
            {...rest}
            element={isAdmin() ? element : <Navigate to="/" />}
        />
    );
};

export default AdminRoute;