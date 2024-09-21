import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import MainPage from './components/MainPage';
// import AdminRoute from './components/AdminRoute';
import AdminComponent from './components/AdminComponent';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './context/AuthContext';


const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/main" element={<MainPage />} />
                <Route path="/" element={<Login />} />
            </Routes>
        </Router>
    );
};

export default App;
