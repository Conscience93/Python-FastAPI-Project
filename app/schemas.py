"""Schema"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

"""Post"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):   #Inheritance
    pass

class PostUpdate(PostBase):
    pass

"""User"""
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Sending info back to user client"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(PostBase):
    id : int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # This will ensure that the thingy will auto convert this into Pydantic when sending response.
        orm_mode = True


"""Access Token"""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
