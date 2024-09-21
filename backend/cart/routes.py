from fastapi import APIRouter, Depends
from database import db
from bson import ObjectId
from models.input import CartItem
from models.output import UserOutput
from auth.utils import get_current_user
from products.utils import convert_objectid_to_str



router = APIRouter()

@router.get("/cart")
async def view_cart(current_user: UserOutput = Depends(get_current_user)):
    print(f'{current_user = }')
    cart = await db["carts"].find_one({"user_id": current_user['_id']})
    if not cart:
        return {"items": []}
    return convert_objectid_to_str(cart)


@router.post("/cart")
async def add_to_cart(item: CartItem, current_user: UserOutput = Depends(get_current_user)):
    # Adicionar item ao carrinho do usuário
    cart = await db["carts"].find_one({"user_id": current_user['_id']})
    if not cart:
        cart = {"user_id": current_user['_id'], "items": []}

    # Verifica se o item já está no carrinho
    for cart_item in cart["items"]:
        if cart_item["product_id"] == item.product_id:
            cart_item["quantity"] += item.quantity
            break
    else:
        cart["items"].append(item.dict())
    
    await db["carts"].update_one({"user_id": current_user['_id']}, {"$set": cart}, upsert=True)
    return {"message": "Item added to cart"}

