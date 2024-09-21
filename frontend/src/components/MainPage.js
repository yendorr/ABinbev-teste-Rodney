import React, { useState } from 'react';
import Products from './Products';
import Cart from './Cart';
import Order from './Order';

const MainPage = () => {
    const [activeTab, setActiveTab] = useState('products');

    const renderTabContent = () => {
        switch (activeTab) {
            case 'products':
                return <Products />;
            case 'cart':
                return <Cart />;
            case 'order':
                return <Order />;
            default:
                return <Products />;
        }
    };

    return (
        <div>
            <h1>Página Principal</h1>
            <div>
                <button onClick={() => setActiveTab('products')}>Produtos</button>
                <button onClick={() => setActiveTab('cart')}>Carrinho</button>
                <button onClick={() => setActiveTab('order')}>Compras Passadas</button>
            </div>
            <div>
                {renderTabContent()}
            </div>
        </div>
    );
};

export default MainPage;
