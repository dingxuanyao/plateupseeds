from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    email: str


class User(UserCreate):
    id: int
    anonymous_name: str = ""

    class Config:
        orm_mode = True


class LikeDelete(BaseModel):
    seed_id: int
    user_id: int


class LikeCreate(LikeDelete):
    is_like: bool


class Like(LikeCreate):
    id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    user_id: int
    seed_id: int
    comment: str


class Comment(CommentCreate):
    id: int
    created_time: datetime

    class Config:
        orm_mode = True


class SeedBase(BaseModel):
    seed_name: str
    seed_type: str
    seed_theme: str


class SeedCreate(SeedBase):
    pass


class Seed(SeedBase):
    id: int
    likes: list[Like] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True
