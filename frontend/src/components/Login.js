import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api'; // Ajuste o caminho se necessário

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const data = await loginUser(username, password);
            setSuccess('Login bem-sucedido!');
            console.log('User logged in:', data);
            localStorage.setItem('authToken', data.access_token); // Armazenando o token
            navigate('/main'); // Redireciona para a página principal ou outra rota
        } catch (err) {
            setError(err.detail || 'Erro ao fazer login.');
        }
    };

    const handleRegisterClick = () => {
        navigate('/register');  // Redireciona para a tela de registro
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            {success && <div style={{ color: 'green' }}>{success}</div>}
            <form onSubmit={handleLogin}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
                <button type="button" onClick={handleRegisterClick}>
                    Registrar
                </button>
            </form>
        </div>
    );
};

export default Login;
