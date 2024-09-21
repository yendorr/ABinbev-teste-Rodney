import axios from 'axios';

// Configure a base URL da sua API
const API_URL = 'http://localhost:8000'; 

// Função para registrar um novo usuário
export const registerUser = async (username, password, isAdmin) => {
    try {
        const response = await axios.post(`${API_URL}/auth/register`, {
            username,
            password,
            isAdmin,
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Função para fazer login
export const loginUser = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/auth/login`, {
            username,
            password,
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

// Função para buscar produtos
export const getProducts = async () => {
    const response = await fetch('http://localhost:8000/products'); // Altere para a URL da sua API
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json(); // Retorna os produtos em formato JSON
};



export const updateProduct = async (id, updatedData) => {
    const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData), // Envie os dados atualizados no corpo da requisição
    });
    if (!response.ok) {
        throw new Error('Failed to update product');
    }
};


export const deleteProduct = async (id) => {
    const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete product');
    }
};

export const addToCart = async (id) => {
    const response = await fetch(`http://localhost:8000/cart/cart`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ productId: id }), // Envie o ID do produto no corpo da requisição
    });
    if (!response.ok) {
        throw new Error('Failed to add product to cart');
    }
};

export const viewCart = async (token) => {
    try {
        const response = await axios.get(`${API_URL}/cart/cart`, {
            headers: {
                Authorization: `Bearer ${token}`, // Altere conforme necessário
            },
        });
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
};

export const getUsers = async () => {
    const response = await fetch('/api/users'); // Altere para a URL correta da sua API
    if (!response.ok) {
        throw new Error('Erro ao buscar usuários');
    }
    return await response.json();
};


export const deleteUser = async (userId) => {
    const response = await fetch(`/api/users/${userId}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Erro ao deletar usuário');
    }
    return await response.json();
};

// Adicione outras funções conforme necessário
