from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.input import UserLogin,UserInput,PasswordChangeInput
from models.output import TokenOutput,UserOutput
from database import db
from auth.utils import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOutput)
async def register(user: UserInput):
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user_data = user.dict()
    user_data["password"] = get_password_hash(user.password)  # Hash da senha
    result = await db["users"].insert_one(user_data)
    return {"id": str(result.inserted_id), **user_data}

@router.post("/login", response_model=TokenOutput)
async def login(user: UserLogin):
    user_db = await db["users"].find_one({"username": user.username})
    if not user_db or not verify_password(user.password, user_db["password"]):  # Verifica o hash
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenOutput)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(password_data: PasswordChangeInput, current_user: UserOutput = Depends(get_current_user)):
    # Verifica se a senha atual está correta
    user_db = await db["users"].find_one({"username": current_user['username']})
    if not user_db or not verify_password(password_data.current_password, user_db["password"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Atualiza a senha
    new_password_hash = get_password_hash(password_data.new_password)
    await db["users"].update_one({"username": current_user['username']}, {"$set": {"password": new_password_hash}})
    
    return {"message": "Password updated successfully"}

@router.delete("/users/{username}", response_model=dict)
async def delete_user(username: str):
    # Verifica se o usuário existe
    user_db = await db["users"].find_one({"username": username})
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Deleta o usuário
    result = await db["users"].delete_one({"username": username})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return {"detail": "User deleted successfully"}





