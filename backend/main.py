from fastapi import FastAPI
from auth.routes import router as auth_router
from products.routes import router as products_router
from cart.routes import router as cart_router
from orders.routes import router as orders_router

from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

# Agora você pode acessar as variáveis de ambiente
mongo_url = os.getenv("MONGO_URL")



app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return {"message": mongo_url}
