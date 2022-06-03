"""Schema"""
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):   #Inheritance
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at: datetime

    class Config:
        # This will ensure that the thingy will auto convert this into Pydantic when sending response.
        orm_mode = True
