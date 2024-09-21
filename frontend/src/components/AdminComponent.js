import React, { useEffect, useState } from 'react';
import { getUsers, deleteUser } from '../api'; // Certifique-se de ajustar o caminho se necessário

const AdminComponent = () => {
    const [users, setUsers] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const data = await getUsers(); // Chama a função para buscar os usuários
                setUsers(data); // Armazena os usuários no estado
            } catch (err) {
                setError('Erro ao carregar usuários.');
                console.error(err);
            }
        };

        fetchUsers(); // Chama a função para buscar usuários quando o componente é montado
    }, []);

    const handleDeleteUser = async (userId) => {
        try {
            await deleteUser(userId); // Chama a função para deletar o usuário
            setUsers(users.filter(user => user.id !== userId)); // Remove o usuário da lista
        } catch (err) {
            setError('Erro ao deletar usuário.');
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Admin Dashboard</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            <h3>Usuários</h3>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>
                        {user.username}
                        <button onClick={() => handleDeleteUser(user.id)}>Remover</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AdminComponent;
