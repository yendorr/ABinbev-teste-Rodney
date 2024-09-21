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

export const createProduct = async (product, token) => {
    try {
        const response = await axios.post(
            `${API_URL}/products/`, 
            product,
            {
                headers: {
                    Authorization: `Bearer ${token}`, // Inclua o token aqui
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error.response.data || 'Erro ao criar produto';
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
    const token = localStorage.getItem('authToken'); // Obtenha o token de autenticação
    const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`, // Adiciona o token ao cabeçalho
            'Content-Type': 'application/json', // Define o tipo de conteúdo
        },
        body: JSON.stringify(updatedData), // Envie os dados atualizados no corpo da requisição
    });
    if (!response.ok) {
        throw new Error('Failed to update product');
    }
};


export const deleteProduct = async (id) => {
    const token = localStorage.getItem('authToken'); // Obtenha o token de autenticação
    const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`, // Adiciona o token ao cabeçalho
            'Content-Type': 'application/json', // Define o tipo de conteúdo
        },
    });

    if (!response.ok) {
        throw new Error('Failed to delete product');
    }
    return await response.json(); // Retorna a resposta se necessário
};

export const addToCart = async (productId, token) => {
    try {
        console.log({ "product_id": productId, "quantity": 1 })
        const response = await axios.post(
            `http://localhost:8000/cart/cart`, 
            { "product_id": productId, "quantity": 1 }, 
            {
                headers: {
                    'Authorization': `Bearer ${token}` // Enviando o token JWT no cabeçalho
                }
            }
        );
        return response.data;
    } catch (error) {
        throw error.response.data || 'Erro ao adicionar ao carrinho';
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
    const response = await fetch('auth/users'); // Altere para a URL correta da sua API
    if (!response.ok) {
        throw new Error('Erro ao buscar usuários');
    }
    return await response.json();
};


export const deleteUser = async (userId) => {
    const response = await fetch(`auth/users/${userId}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Erro ao deletar usuário');
    }
    return await response.json();
};

