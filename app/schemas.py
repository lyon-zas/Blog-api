from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional 
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id:int
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)