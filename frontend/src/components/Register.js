import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../api'; // Certifique-se de ajustar o caminho se necessário

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isAdmin, setIsAdmin] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate(); // Alterado para useNavigate

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const data = await registerUser(username, password, isAdmin);
            setSuccess('Usuário registrado com sucesso!');
            console.log('User registered:', data);

            // Redireciona para a página de login após o registro bem-sucedido
            navigate('/login'); // Alterado para navigate
        } catch (err) {
            setError(err.detail || 'Erro ao registrar usuário.');
        }
    };

    return (
        <div>
            <h2>Registrar</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            {success && <div style={{ color: 'green' }}>{success}</div>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Nome de usuário:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Senha:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>
                        <input
                            type="checkbox"
                            checked={isAdmin}
                            onChange={() => setIsAdmin(!isAdmin)}
                        />
                        Administrador
                    </label>
                </div>
                <button type="submit">Registrar</button>
            </form>
        </div>
    );
};

export default Register;
