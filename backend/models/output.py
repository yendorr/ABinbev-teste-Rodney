from pydantic import BaseModel

class TokenOutput(BaseModel):
    access_token: str
    token_type: str


class UserOutput(BaseModel):
    id: str
    username: str
    is_admin: bool


class ProductOutput(BaseModel):
    id: str
    name: str
    price: float
