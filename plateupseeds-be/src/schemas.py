from pickletools import int4
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class SeedBase(BaseModel):
    seed_name: str
    seed_type: str


class SeedCreate(SeedBase):
    pass


class Seed(SeedBase):
    id: int

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


# class DislikesCreate(BaseModel):
#     user_id: int
#     seed_id: int


# class Dislikes(DislikesCreate):
#     id: int

#     class Config:
#         orm_mode = True
