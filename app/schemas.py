"""Schema"""
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
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

class PostOut(PostBase):
    Post: Post
    votes: int
    # this is because in db.query, it returns a dictionary post, Post: {id: 13, published: True, etc.etc.}, votes: 0

    class Config:
        orm_mode = True

"""Access Token"""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

"""Vote"""
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=1)    # 0 or 1 only