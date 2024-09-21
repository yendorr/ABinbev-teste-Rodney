from fastapi import APIRouter, Depends
from database import db

router = APIRouter()

@router.post("/")
async def place_order(user: str):
    cart_items = await db["cart"].find({"user_id": user}).to_list(100)
    await db["orders"].insert_one({"user_id": user, "items": cart_items})
    return {"msg": "Order placed successfully"}

@router.get("/")
async def list_orders(user: str):
    orders = await db["orders"].find({"user_id": user}).to_list(100)
    return orders
