from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Tokens(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int
    user_id: int

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True