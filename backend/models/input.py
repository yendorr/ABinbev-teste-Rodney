from pydantic import BaseModel

class UserInput(BaseModel):
    username: str
    password: str
    is_admin: bool = False  # Por padrão, não é admin

class UserLogin(BaseModel):
    username: str
    password: str


class ProductInput(BaseModel):
    name: str
    price: float
