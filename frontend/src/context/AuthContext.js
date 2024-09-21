import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // ou um objeto com as informações do usuário

    const login = (userData) => {
        setUser(userData); // Salva as informações do usuário após login
    };

    const logout = () => {
        setUser(null); // Limpa as informações do usuário
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};