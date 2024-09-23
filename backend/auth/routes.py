from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.input import UserLogin,UserInput,PasswordChangeInput
from models.output import TokenOutput,UserOutput
from database import db
from auth.utils import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOutput)
async def register(user: UserInput):
    """
    Registers a new user in the system.

    Args:
        user (UserInput): The input data for creating a new user, including username and password.

    Returns:
        dict: A dictionary containing the `id` of the newly registered user and their user data.

    Raises:
        HTTPException: If the username is already registered, raises a 409 HTTP exception with a message.
    """
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    user_data = user.dict()
    user_data["password"] = get_password_hash(user.password)  # Hash da senha
    result = await db["users"].insert_one(user_data)
    return {"id": str(result.inserted_id), **user_data}

@router.post("/login", response_model=TokenOutput)
async def login(user: UserLogin):
    """
    Authenticate a user and return an access token.

    Args:
        user (UserLogin): The user credentials containing the username and password.

    Returns:
        TokenOutput: An object containing the access token and token type.

    Raises:
        HTTPException: If the credentials are invalid, a 401 Unauthorized exception is raised.
    """

    user_db = await db["users"].find_one({"username": user.username})
    if not user_db or not verify_password(user.password, user_db["password"]): 
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenOutput)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Obtain an access token by authenticating the user with their credentials.

    Args:
        form_data (OAuth2PasswordRequestForm): The user's login credentials, including username and password.

    Returns:
        TokenOutput: An object containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect, a 401 Unauthorized exception is raised.
    """

    user = await db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(password_data: PasswordChangeInput, current_user: UserOutput = Depends(get_current_user)):
    """
    Change the user's password after verifying the current password.

    Args:
        password_data (PasswordChangeInput): Contains the current and new passwords.
        current_user (UserOutput): The current authenticated user, obtained from the dependency.

    Returns:
        dict: A message confirming that the password has been updated successfully.

    Raises:
        HTTPException: If the current password is incorrect, a 401 Unauthorized exception is raised.
    """

    # Verifica se a senha atual está correta
    user_db = await db["users"].find_one({"username": current_user['username']})
    if not user_db or not verify_password(password_data.current_password, user_db["password"]):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Atualiza a senha
    new_password_hash = get_password_hash(password_data.new_password)
    await db["users"].update_one({"username": current_user['username']}, {"$set": {"password": new_password_hash}})
    
    return {"message": "Password updated successfully"}

@router.delete("/users/{username}", response_model=dict)
async def delete_user(username: str):
    """
    Delete a user from the database.

    Args:
        username (str): The username of the user to be deleted.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: Raises a 404 error if the user is not found.
        HTTPException: Raises a 500 error if the deletion fails.
    """

    # Verifica se o usuário existe
    user_db = await db["users"].find_one({"username": username})
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Deleta o usuário
    result = await db["users"].delete_one({"username": username})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return {"detail": "User deleted successfully"}





