// src/components/PrivateRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = ({ children, requiredRole }) => {
    const { user } = useAuth();

    if (!user) {
        // Redireciona para a página de login se o usuário não estiver logado
        return <Navigate to="/login" />;
    }

    if (requiredRole && !user.isAdmin) {
        // Redireciona para a página principal se o usuário não tiver a role necessária
        return <Navigate to="/" />;
    }

    // Renderiza os componentes filhos (a rota protegida)
    return children;
};

export default PrivateRoute;
