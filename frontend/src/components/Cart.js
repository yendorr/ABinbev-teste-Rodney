import React, { useEffect, useState } from 'react';
import { getCartItems, finalizeOrder } from '../api'; // Ajuste o caminho se necessário

const Cart = () => {
    const [cartItems, setCartItems] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        const fetchCartItems = async () => {
            try {
                const data = await getCartItems(); // Obtenha os itens do carrinho
                console.log('Cart items:', data); // Inspecione os dados retornados
                setCartItems(data.items || []); // Use a propriedade items se existir
            } catch (err) {
                setError('Erro ao carregar itens do carrinho.');
                console.error(err);
            }
        };

        fetchCartItems(); // Chama a função ao montar o componente
    }, []);

    const handleFinalizeOrder = async () => {
        try {
            await finalizeOrder(); // Chama a rota para finalizar a compra
            setSuccess('Compra finalizada com sucesso!');
            setCartItems([]); // Limpa o carrinho após finalizar a compra
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
                            Produto ID: {item.product_id} - Quantidade: {item.quantity}
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
