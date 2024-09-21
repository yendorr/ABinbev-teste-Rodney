import React, { useEffect, useState } from 'react';
import { getProducts, deleteProduct, addToCart, updateProduct, createProduct } from '../api'; 

const Products = () => {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState('');
    const [editingProduct, setEditingProduct] = useState(null);
    const [updatedName, setUpdatedName] = useState('');
    const [updatedPrice, setUpdatedPrice] = useState('');
    const [newProductName, setNewProductName] = useState('');
    const [newProductPrice, setNewProductPrice] = useState('');

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
            setProducts(products.filter((product) => product._id !== id));
        } catch (err) {
            setError('Erro ao remover o produto.',err.detail);
            console.error(err);
        }
    };

    const handleAddToCart = async (productId) => {
        console.log("ala", productId)
        try {
            const token = localStorage.getItem('authToken'); // Pegando o token
            if (!token) throw new Error('Usuário não autenticado');
            console.log('Token:', token);
            await addToCart(productId, token);
            alert('Produto adicionado ao carrinho!');
        } catch (err) {
            setError('Erro ao adicionar produto ao carrinho.');
            console.error(err);
        }
    };

    const handleEdit = (product) => {
        setEditingProduct(product);
        setUpdatedName(product.name);
        setUpdatedPrice(product.price); // Preenche o campo com o preço atual
    };

    const handleUpdate = async (id) => {
        try {
            await updateProduct(id, { name: updatedName, price: updatedPrice }); // Chama a função de atualização
            setProducts(products.map((product) => 
                (product._id === id ? { ...product, name: updatedName, price: updatedPrice } : product)
            )); // Atualiza a lista
            setEditingProduct(null); // Fecha o modo de edição
            setUpdatedName(''); // Limpa os campos
            setUpdatedPrice('');
        } catch (err) {
            setError('Erro ao atualizar o produto.');
            console.error(err);
        }
    };

    const handleCreate = async () => {
        try {
            const token = localStorage.getItem('authToken'); // Pegando o token
            const newProduct = await createProduct({ name: newProductName, price: newProductPrice },token);
            const newProduct2 = { _id: newProduct.id, name: newProductName, price: newProductPrice };
            setProducts([...products, newProduct2]); // Adiciona o novo produto à lista
            setNewProductName(''); // Limpa os campos
            setNewProductPrice('');
        } catch (err) {
            setError('Erro ao adicionar o novo produto.', err);
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Produtos</h2>
            {error && <div style={{ color: 'red' }}>{error}</div>}

            {/* Formulário para adicionar novo produto */}
            <div>
                <h3>Adicionar Novo Produto</h3>
                <input
                    type="text"
                    placeholder="Nome do produto"
                    value={newProductName}
                    onChange={(e) => setNewProductName(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Preço do produto"
                    value={newProductPrice}
                    onChange={(e) => setNewProductPrice(e.target.value)}
                />
                <button onClick={handleCreate}>Adicionar Produto</button>
            </div>

            <ul>
                {products.map((product) => (
        
                    <li key={product._id}>
                        {editingProduct && editingProduct._id === product._id ? (
                            <div>
                                <input
                                    type="text"
                                    value={updatedName}
                                    onChange={(e) => setUpdatedName(e.target.value)}
                                />
                                <input
                                    type="number"
                                    value={updatedPrice}
                                    onChange={(e) => setUpdatedPrice(e.target.value)}
                                />
                                <button onClick={() => handleUpdate(product._id)}>Atualizar</button>
                                <button onClick={() => setEditingProduct(null)}>Cancelar</button>
                            </div>
                        ) : (
                            <div>
                                {product.name} - R$ {product.price} - 
                                <button onClick={() => handleEdit(product)}>Editar</button>
                                <button onClick={() => handleDelete(product._id)}>Remover</button>
                                <button onClick={() => handleAddToCart(product._id)}>Adicionar ao Carrinho</button>
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Products;
