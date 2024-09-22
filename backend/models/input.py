from pydantic import BaseModel
from typing import List


class UserInput(BaseModel):
    username: str
    password: str
    is_admin: bool

class PasswordChangeInput(BaseModel):
    current_password: str
    new_password: str

class UserLogin(BaseModel):
    username: str
    password: str


class ProductInput(BaseModel):
    name: str
    price: float


class CartItem(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: List[CartItem]

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Order(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float
