import os
import pytest
import motor.motor_asyncio  # Driver assíncrono do MongoDB

from fastapi.testclient import TestClient
from main import app  # Ajuste conforme o nome do seu arquivo principal
import asyncio

# Configure a URL do MongoDB para testes
os.environ["MONGO_URL"] = "mongodb://mongo_test:27017/ecom_db"

@pytest.fixture(scope="session", autouse=True)
def mongo_cleanup():
    try:
        # Conectar ao MongoDB
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
        

        db = mongo_client["ecom_db"]

        # Limpar o banco de dados antes dos testes
        mongo_client.drop_database("ecom_db")  # Limpa o banco de dados corretamente

        yield  # Isso permite que os testes sejam executados

    except Exception as e:
        print(f"Erro ao conectar ou limpar o banco de dados: {e}")

    finally:
        # Limpar o banco de dados após os testes
        mongo_client.drop_database("ecom_db") # Limpa o banco de dados novamente
        mongo_client.close()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

#TO DO solve the closing loop issue and split this funtion 
def tests(client):
    #user tests
    response = client.post(
        "/auth/register", 
        json={"username": "testAdminUser", "password": "testPassword", "is_admin": True}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testAdminUser"

    response = client.post(
        "/auth/register", 
        json={"username": "testAdminUser", "password": "testPassword", "is_admin": True}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already registered"

    response = client.post(
        "/auth/register", 
        json={"username": "testUser", "password": "testPassword", "is_admin": False}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testUser"

    response = client.post(
        "/auth/login",
        json={"username": "nonexistentUser", "password": "testPassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    response = client.post(
        "/auth/login",
        json={"username": "testAdminUser", "password": "testPassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    admin_token = response.json()["access_token"]

    response = client.post(
        "/auth/login",
        json={"username": "testUser", "password": "testPassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    normal_token = response.json()["access_token"]
    

    response = client.post(
        "/auth/change-password",
        json={"current_password": "testPassword", "new_password": "newPassword"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    response = client.post(
        "/auth/login",
        json={"username": "testAdminUser", "password": "newPassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = client.delete("/auth/users/testAdminUser")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"

    response = client.post(
        "/auth/login",
        json={"username": "testAdminUser", "password": "newPassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    response = client.post(
        "/auth/register",
        json={"username": "testAdminUser", "password": "testPassword", "is_admin": True}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testAdminUser"

    response = client.post(
        "/auth/login",
        json={"username": "testAdminUser", "password": "testPassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    admin_token = response.json()["access_token"]

    ########################

    response = client.post(
        "/products/",
        json={"name": "testProduct", "price": 10.00},
        headers={"Authorization": f"Bearer {normal_token}"} 
    )
    assert response.status_code == 403

    response = client.post(
        "/products/",
        json={"name": "testProduct", "price": 10.00},
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200
    assert response.json()["name"] == "testProduct"
    assert "id" in response.json()
    assert response.json()["price"] == 10.00
    product_id = response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"name": "newProduct", "price": 5.00},
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200
    assert response.json()["name"] == "newProduct"
    assert response.json()["price"] == 5.00

    response = client.put(
        f"/products/{product_id}",
        json={"name": "newProduct", "price": 5.00},
        headers={"Authorization": f"Bearer {normal_token}"} 
    )
    assert response.status_code == 403

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "newProduct"
    assert response.json()["price"] == 5.00

    response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200

    # response = client.get(f"/products/{product_id}")
    # assert response.status_code == 404

    response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post(
        "/products/",
        json={"name": "testProduct", "price": 10.00},
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200
    assert response.json()["name"] == "testProduct"
    assert "id" in response.json()
    assert response.json()["price"] == 10.00
    product_id = response.json()["id"]

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"} 
    )
    assert response.status_code == 200
    assert response.json()["name"] == "testProduct"

    #################

    response = client.post(
        f"/cart/",
        json={"product_id": product_id,"quantity": 1},
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Item added to cart"

    response = client.post(
        f"/cart/",
        json={"product_id": product_id,"quantity": 1},
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Item added to cart"

    response = client.get(
        "/cart",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    

    response = client.post(
        f"/cart/order/",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Order placed successfully"

    
    response = client.get(
        "/cart",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0
    
    response = client.get(
        "/orders",
        headers={"Authorization": f"Bearer {normal_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["items"][0]["product_id"] == product_id
    assert response.json()[0]["items"][0]["quantity"] == 2
    assert response.json()[0]["items"][0]["price"] == 10.00
    assert response.json()[0]["total"] == 20.00
