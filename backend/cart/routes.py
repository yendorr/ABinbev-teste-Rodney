from fastapi import APIRouter, Depends, HTTPException
from database import db
from bson import ObjectId
from models.input import CartItem
from models.output import UserOutput
from auth.utils import get_current_user
from products.utils import convert_objectid_to_str



router = APIRouter()

@router.get("/")
async def view_cart(current_user: UserOutput = Depends(get_current_user)):
    """
    Retrieve the current user's cart.

    Args:
        current_user (UserOutput): The user whose cart is being accessed, obtained through the authentication token.

    Returns:
        dict: A dictionary representing the user's cart. If the cart is empty, it returns an empty list under the "items" key.

    Raises:
        HTTPException: Raises a 401 Unauthorized exception if the user cannot be authenticated.
    """

    cart = await db["carts"].find_one({"user_id": current_user['_id']})
    if not cart:
        return {"items": []}
    return convert_objectid_to_str(cart)


@router.post("/")
async def add_to_cart(item: CartItem, current_user: UserOutput = Depends(get_current_user)):
    """
    Add an item to the current user's cart.

    Args:
        item (CartItem): The item to be added to the cart, which includes the product ID and quantity.
        current_user (UserOutput): The user who is adding the item to their cart, obtained through the authentication token.

    Returns:
        dict: A message indicating that the item has been added to the cart.

    Raises:
        HTTPException: Raises a 401 Unauthorized exception if the user cannot be authenticated.
    """

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


@router.post("/order")
async def place_order(current_user: UserOutput = Depends(get_current_user)):
    """
    Places an order for the current user by moving items from their cart to an order and clearing the cart.

    Args:
        current_user (UserOutput): The authenticated user who is placing the order, obtained through the authentication token.

    Returns:
        dict: A confirmation message along with the order details, including the user ID, items, and total cost.

    Raises:
        HTTPException: Raises a 400 exception if the cart is empty.
        HTTPException: Raises a 404 exception if a product in the cart is not found (currently continues instead).
    """

    cart = await db["carts"].find_one({"user_id": current_user['_id']})
    if not cart or not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in cart["items"]:
        product = await db["products"].find_one({"_id": ObjectId(item["product_id"])})
        if not product:
            print("Product not found: " + item["product_id"])
            print("Continuing to next item...")
            continue

        order_items.append({
            "product_id": str(item["product_id"]),  # Convertendo para string
            "quantity": item["quantity"],
            "price": product["price"]
        })
        total += item["quantity"] * product["price"]

    order = {
        "user_id": str(current_user['_id']),  # Convertendo para string
        "items": order_items,
        "total": total
    }

    await db["orders"].insert_one(order)
    await db["carts"].delete_one({"user_id": current_user['_id']})
    
    return {
        "message": "Order placed successfully",
        "order": {
            "user_id": order["user_id"],
            "items": order_items,
            "total": order["total"]
        }
    }
