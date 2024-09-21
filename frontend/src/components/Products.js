import React, { useEffect, useState } from 'react';
import { getProducts, deleteProduct, addToCart, updateProduct } from '../api'; // Ajuste o caminho se necessário

const Products = () => {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState('');
    const [editingProduct, setEditingProduct] = useState(null);
    const [updatedName, setUpdatedName] = useState('');

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await getProducts();
                setProducts(data);
            } catch (err) {
                setError('Erro ao carregar produtos.');
                console.error(err);
            }
        };

        fetchProducts();
    }, []);

    const handleDelete = async (id) => {
        try {
            await deleteProduct(id);
            setProducts(products.filter((product) => product.id !== id));
        } catch (err) {
            setError('Erro ao remover o produto.');
            console.error(err);
        }
    };

    const handleAddToCart = async (id) => {
        try {
            await addToCart(id);
            alert('Produto adicionado ao carrinho!');
        } catch (err) {
            setError('Erro ao adicionar o produto ao carrinho.');
            console.error(err);
        }
    };

    const handleEdit = (product) => {
        setEditingProduct(product);
        setUpdatedName(product.name); // Preenche o campo com o nome atual
    };

    const handleUpdate = async (id) => {
        try {
            await updateProduct(id, { name: updatedName }); // Chama a função de atualização
            setProducts(products.map((product) => (product.id === id ? { ...product, name: updatedName } : product))); // Atualiza a lista
            setEditingProduct(null); // Fecha o modo de edição
            setUpdatedName(''); // Limpa o campo
        } catch (err) {
            setError('Erro ao atualizar o produto.');
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Produtos</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
                        {editingProduct && editingProduct.id === product.id ? (
                            <div>
                                <input
                                    type="text"
                                    value={updatedName}
                                    onChange={(e) => setUpdatedName(e.target.value)}
                                />
                                <button onClick={() => handleUpdate(product.id)}>Atualizar</button>
                                <button onClick={() => setEditingProduct(null)}>Cancelar</button>
                            </div>
                        ) : (
                            <div>
                                {product.name}
                                <button onClick={() => handleEdit(product)}>Editar</button>
                                <button onClick={() => handleDelete(product.id)}>Remover</button>
                                <button onClick={() => handleAddToCart(product.id)}>Adicionar ao Carrinho</button>
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Products;
