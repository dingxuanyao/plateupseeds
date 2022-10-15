from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, true, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

from .database import Base

from sqlalchemy import select


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    anonymous_name = Column(String)


class Seed(Base):
    __tablename__ = "seeds"

    id = Column(Integer, primary_key=True, index=True)
    seed_name = Column(String, unique=True, index=True)
    seed_type = Column(String)
    likes = relationship("Like")

    @hybrid_property
    def like_count(self):
        likes = [_ for _ in self.likes if _.is_like]
        return len(likes)

    @like_count.expression
    def like_count(cls):
        return (select([func.count(Like.id)])
                .where(Like.seed_id == cls.id)
                .where(Like.is_like == True)
                .label("like_count"))

    def __repr__(self) -> str:
        return f"Seed(id={self.id}, seed_name={self.seed_name}, seed_type={self.seed_type}, like_count={self.like_count})"


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seed_id = Column(Integer, ForeignKey("seeds.id"))
    is_like = Column(Boolean)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_time = Column(DateTime)
    comment = Column(String)



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
