from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from models.output import UserOutput
from database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    """
    Generate a hashed password.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed version of the password.

    Raises:
        ValueError: Raises an exception if the password is empty.
    """
    
    if not password:
        raise ValueError("Password cannot be empty")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.

    Raises:
        ValueError: Raises an exception if the plaintext password or hashed password is empty.
    """
    
    if not plain_password or not hashed_password:
        raise ValueError("Passwords cannot be empty")
    
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with an expiration time.

    Args:
        data (dict): A dictionary containing the data to encode in the token.
        expires_delta (Optional[timedelta]): The duration for which the token will be valid. If not provided, defaults to the value set by ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT access token.

    Raises:
        Exception: Raises an exception if token encoding fails.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user from the provided token.

    Args:
        token (str): The access token used for authentication.

    Returns:
        dict: The user information retrieved from the database.

    Raises:
        HTTPException: Raises a 401 error if the token is invalid or the user is not found.
                       Raises a 404 error if the user does not exist.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = await db["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def check_admin(current_user: UserOutput = Depends(get_current_user)):
    """
    Check if the current user has admin privileges.

    Args:
        current_user (UserOutput): The current user retrieved from the authentication token.

    Returns:
        None: This function does not return a value. It raises an exception if the user is not an admin.

    Raises:
        HTTPException: Raises a 403 error if the current user does not have admin permissions.
    """

    if not current_user['is_admin']:
        raise HTTPException(status_code=403, detail="Not enough permissions")

