import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // Armazena os dados do usuário logado

    const login = (userData) => {
        setUser(userData); // Configura os dados do usuário logado
    };

    const logout = () => {
        setUser(null); // Limpa os dados do usuário
    };

    const isAdmin = () => {
        return user && user.isAdmin; // Verifica se o usuário é admin
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAdmin }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
