import React, { useEffect, useState } from 'react';
import { getOrders, getProductById } from '../api'; // Certifique-se de ajustar o caminho se necessário

const Order = () => {
    const [orders, setOrders] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const data = await getOrders(); // Chama a função para buscar as ordens
                // Para cada item de cada pedido, busque o nome e preço do produto
                const ordersWithProductDetails = await Promise.all(
                    data.map(async (order) => {
                        const itemsWithDetails = await Promise.all(
                            order.items.map(async (item) => {
                                try {
                                    // Tenta buscar o nome e preço do produto pelo product_id
                                    const product = await getProductById(item.product_id);
                                    return {
                                        ...item,
                                        product_name: product ? product.name : item.product_id,
                                        product_price: product ? product.price : 0, // Se o preço for encontrado, usa o preço, senão usa 0
                                    };
                                } catch (err) {
                                    console.error(`Erro ao buscar o produto com ID ${item.product_id}:`, err);
                                    return { ...item, product_name: item.product_id, product_price: 0 }; // Retorna 0 se der erro
                                }
                            })
                        );
                        return { ...order, items: itemsWithDetails };
                    })
                );
                setOrders(ordersWithProductDetails); // Armazena as ordens com detalhes dos produtos
            } catch (err) {
                setError('Erro ao carregar ordens.');
                console.error(err);
            }
        };

        fetchOrders(); // Chama a função para buscar ordens quando o componente é montado
    }, []);

    // Função para calcular o total da compra
    const calculateTotal = (items) => {
        return items.reduce((total, item) => total + item.product_price * item.quantity, 0);
    };

    return (
        <div>
            <h2>Compras Passadas</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            <ul>
                {orders.map((order) => (
                    <li key={order._id}>
                        <div>
                            <strong>ID:</strong> {order._id}<br />
                            {/* <strong>Data:</strong> {new Date(order.createdAt).toLocaleDateString()}<br /> */}
                            <strong>Itens:</strong>
                            <ul>
                                {order.items.map((item, index) => (
                                    <li key={index}>
                                        Produto: {item.product_name}, Quantidade: {item.quantity}, Preço: R$ {item.product_price.toFixed(2)}
                                    </li>
                                ))}
                            </ul>
                            <strong>Total:</strong> R$ {calculateTotal(order.items).toFixed(2)}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Order;
