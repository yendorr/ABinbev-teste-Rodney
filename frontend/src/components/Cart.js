import React, { useEffect, useState } from 'react';
import { getCartItems, getProductById, finalizeOrder } from '../api'; // Ajuste o caminho se necessário

const Cart = () => {
    const [cartItems, setCartItems] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [productNames, setProductNames] = useState({}); // Estado para armazenar os nomes dos produtos

    useEffect(() => {
        const fetchCartItems = async () => {
            try {
                const data = await getCartItems();
                setCartItems(data.items || []);
                await fetchProductNames(data.items); // Chama a função para buscar os nomes dos produtos
            } catch (err) {
                setError('Erro ao carregar itens do carrinho.');
                console.error(err);
            }
        };

        fetchCartItems();
    }, []);

    const fetchProductNames = async (items) => {
        const names = {};
        for (const item of items) {
            try {
                const product = await getProductById(item.product_id); // Busca o produto pelo ID
                names[item.product_id] = product.name; // Armazena o nome do produto
            } catch (err) {
                console.error(`Erro ao buscar produto ${item.product_id}:`, err);
            }
        }
        setProductNames(names); // Atualiza o estado com os nomes dos produtos
    };

    const handleFinalizeOrder = async () => {
        try {
            await finalizeOrder();
            setSuccess('Compra finalizada com sucesso!');
            setCartItems([]); // Limpa o carrinho após finalizar a compra
            setProductNames({}); // Limpa os nomes dos produtos
        } catch (err) {
            setError('Erro ao finalizar a compra.');
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Carrinho</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            {success && <div style={{ color: 'green' }}>{success}</div>}
            {cartItems.length === 0 ? (
                <p>Seu carrinho está vazio.</p>
            ) : (
                <ul>
                    {cartItems.map((item) => (
                        <li key={item.product_id}>
                            {productNames[item.product_id] || 'Carregando...'} - Quantidade: {item.quantity}
                        </li>
                    ))}
                </ul>
            )}
            <button onClick={handleFinalizeOrder} disabled={cartItems.length === 0}>
                Finalizar Compra
            </button>
        </div>
    );
};

export default Cart;
