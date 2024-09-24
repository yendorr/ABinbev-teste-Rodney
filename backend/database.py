from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

mongo_url = os.getenv("MONGO_URL")


def get_db():
    client = AsyncIOMotorClient(mongo_url)
    return client['ecom_db']
db = get_db()