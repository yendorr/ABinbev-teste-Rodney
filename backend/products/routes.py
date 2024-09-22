from fastapi import APIRouter, Depends, HTTPException
from models.input import ProductInput
from models.output import ProductOutput
from products.utils import convert_objectid_to_str
from database import db
from bson import ObjectId
from auth.utils import check_admin


router = APIRouter()

@router.get("/")
async def list_products():
    products = await db["products"].find().to_list(100)
    return convert_objectid_to_str(products)

@router.get("/{product_id}")
async def get_product_by_id(product_id: str):
    try:
        # Converte a string para ObjectId
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
        if product is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return convert_objectid_to_str(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=ProductOutput, dependencies=[Depends(check_admin)])
async def add_product(product: ProductInput):
    product_data = product.dict()
    result = await db["products"].insert_one(product_data)
    return {"id": str(result.inserted_id), **product_data}

@router.put("/{product_id}", response_model=ProductOutput, dependencies=[Depends(check_admin)])
async def edit_product(product_id: str, product: ProductInput):
    # Converte o modelo de produto para um dicionário
    product_data = product.dict(exclude_unset=True)  # Exclui campos que não foram enviados na requisição

    # Tenta atualizar o produto no banco de dados
    result = await db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product_data}
    )

    # Verifica se o produto foi encontrado e atualizado
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    # Retorna o produto atualizado
    updated_product = await db["products"].find_one({"_id": ObjectId(product_id)})
    
    # Converte o ObjectId para string e renomeia _id para id
    updated_product["id"] = str(updated_product["_id"])
    del updated_product["_id"]
    
    return updated_product


@router.delete("/{product_id}", response_model=dict, dependencies=[Depends(check_admin)])
async def delete_product(product_id: str):
    result = await db["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    

