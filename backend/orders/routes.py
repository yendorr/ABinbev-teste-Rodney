from fastapi import APIRouter, Depends
from auth.utils import get_current_user
from models.output import UserOutput
from database import db
from products.utils import convert_objectid_to_str

router = APIRouter()

@router.get("/", response_model=list)
async def list_orders(current_user: UserOutput = Depends(get_current_user)):
    """
    Retrieves a list of orders placed by the current user.

    Args:
        current_user (UserOutput): The authenticated user, obtained through the authentication token.

    Returns:
        list: A list of orders, where each order contains the order details including order ID, items, and total cost. All ObjectId fields are converted to strings.

    Raises:
        KeyError: Raises an exception if there is an issue retrieving the current user.
    """

    # Busca as ordens do usuário no banco de dados
    print(current_user)
    orders = await db["orders"].find({"user_id": str(current_user['_id'])}).to_list(100)
    
    # Converte ObjectId para string, se necessário
    for order in orders:
        order['_id'] = str(order['_id'])  # Converte o ObjectId para string
        for item in order["items"]:
            item["product_id"] = str(item["product_id"])  # Converte product_id para string

    return convert_objectid_to_str(orders)

