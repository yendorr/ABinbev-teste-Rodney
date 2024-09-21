import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import MainPage from './components/MainPage';
// import AdminRoute from './components/AdminRoute';
import AdminComponent from './components/AdminComponent';
import { AuthProvider } from './AuthContext';


const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/main" element={<MainPage />} />
                {/* <AdminRoute path="/admin" element={<AdminComponent />} /> Rota admin */}
                <Route path="/" element={<Login />} />
            </Routes>
        </Router>
    );
};

export default App;
