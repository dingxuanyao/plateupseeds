from optparse import Values
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)



class Seed(Base):
    __tablename__ = "seeds"

    id = Column(Integer, primary_key=True, index=True)
    seed_name = Column(String, unique=True, index=True)
    seed_type = Column(String)
    like_count = Column(Integer, default=0)


## TODO: likes and dislikes instead
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seed_id = Column(Integer, ForeignKey("seeds.id"))
    is_like = Column(Boolean)

# class Like(Base):
#     __tablename__ = "likes"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     seed_id = Column(Integer, ForeignKey("seeds.id"))

#     __table_args__ = (UniqueConstraint('user_id', 'seed_id', name='_user_seed_likes_uc'),)

# class Dislike(Base):
#     __tablename__ = "dislikes"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     seed_id = Column(Integer, ForeignKey("seeds.id"))

#     __table_args__ = (UniqueConstraint('user_id', 'seed_id', name='_user_seed_dislikes_uc'),)
