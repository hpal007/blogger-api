from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: str
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
