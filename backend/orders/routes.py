from fastapi import APIRouter, Depends
from auth.utils import get_current_user
from models.output import UserOutput
from database import db
from products.utils import convert_objectid_to_str

# db.<nome_da_colecao>.find().pretty()
router = APIRouter()

@router.get("/", response_model=list)
async def list_orders(current_user: UserOutput = Depends(get_current_user)):
    """
This is an example of Google style.

Args:
    param1: This is the first param.
    param2: This is a second param.

Returns:
    This is a description of what is returned.

Raises:
    KeyError: Raises an exception.
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
