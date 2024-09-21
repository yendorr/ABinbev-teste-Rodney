from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

# Agora você pode acessar as variáveis de ambiente
mongo_url = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(mongo_url)
db = client['ecom_db']