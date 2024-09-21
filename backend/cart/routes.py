from fastapi import APIRouter, Depends
from database import db
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def add_to_cart(product_id: str, user: str):
    await db["cart"].insert_one({"user_id": user, "product_id": ObjectId(product_id)})
    return {"msg": "Product added to cart"}

@router.get("/")
async def view_cart(user: str):
    cart_items = await db["cart"].find({"user_id": user}).to_list(100)
    return cart_items
