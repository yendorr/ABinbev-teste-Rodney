from fastapi import APIRouter, Depends, HTTPException
from models.input import UserLogin,UserInput
from models.output import TokenOutput,UserOutput
from database import db
from auth.utils import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOutput)
async def register(user: UserInput):
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user_data = user.dict()
    result = await db["users"].insert_one(user_data)
    return {"id": str(result.inserted_id), **user_data}

@router.post("/login", response_model=TokenOutput)
async def login(user: UserLogin):
    user_db = await db["users"].find_one({"username": user.username})
    if not user_db or not verify_password(user.password, user_db["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
