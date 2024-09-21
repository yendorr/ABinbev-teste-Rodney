from fastapi import APIRouter, HTTPException
from models.input import ProductInput
from models.output import ProductOutput
from products.utils import convert_objectid_to_str
from database import db
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def list_products():
    products = await db["products"].find().to_list(100)
    return convert_objectid_to_str(products)

@router.post("/", response_model=ProductOutput)
async def add_product(product: ProductInput):
    product_data = product.dict()
    result = await db["products"].insert_one(product_data)
    return {"id": str(result.inserted_id), **product_data}

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    result = await db["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        return {"error": "Product not found"}, 404
