from pydantic import BaseModel
from typing import Optional, List

# Item Schemas
class ItemBase(BaseModel):
    category: str
    occasion: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    image_filename: str
    color: str
    user_id: int

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    items: List[ItemResponse] = []

    class Config:
        orm_mode = True
