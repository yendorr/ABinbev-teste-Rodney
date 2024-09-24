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

def test_register_user(client):
    response = client.post("/auth/register", json={"username": "testUser", "password": "testPassword", "is_admin": True})
    assert response.status_code == 200
    assert response.json()["username"] == "testUser"

def test_register_user2(client):
    response = client.post("/auth/register", json={"username": "testUser", "password": "testPassword", "is_admin": True})
    assert response.status_code == 200
    assert response.json()["username"] == "testUser"
