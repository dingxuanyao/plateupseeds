from ast import Str
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_seeds(db: Session, seed_type: Str,  skip: int = 0, limit: int = 100):

    # sorted by number of likes
    seeds = db.query(models.Seed).filter(
        models.Seed.seed_type == seed_type).order_by(
        models.Seed.like_count.desc()).offset(skip).limit(limit).all()

    return seeds
    # return db.query(models.Seed).filter(models.Seed.seed_type == seed_type).order_by(models.Seed.likes.desc()).offset(skip).limit(limit).all()
    return db.query(models.Seed).filter(models.Seed.seed_type == seed_type).offset(skip).limit(limit).all()


def get_seed(db: Session, seed_name: str,):
    return db.query(models.Seed).filter(models.Seed.seed_name == seed_name).first()


def create_seed(db: Session, seed: schemas.SeedCreate):
    db_seed = models.Seed(**seed.dict())
    db.add(db_seed)
    db.commit()
    db.refresh(db_seed)
    return db_seed


def get_likes(db: Session, seed_name: str):
    seed_id = db.query(models.Seed).filter(
        models.Seed.seed_name == seed_name).first().id
    return db.query(models.Like).filter(models.Like.seed_id == seed_id).all()


def upsert_like(db: Session, like: schemas.LikeCreate):
    db_like = db.query(models.Like).filter(
        models.Like.user_id == like.user_id,
        models.Like.seed_id == like.seed_id
    ).first()
    if db_like:
        db_like.is_like = like.is_like
    else:
        db_like = models.Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)

    # update seed like count
    update_seed_like_count(db, like)

    return db_like


def delete_like(db: Session, like: schemas.LikeCreate):
    db_like = db.query(models.Like).filter(
        models.Like.user_id == like.user_id).filter(
        models.Like.seed_id == like.seed_id).first()
    db.delete(db_like)
    db.commit()

    # update seed like count
    update_seed_like_count(db, like)
    return db_like


def update_seed_like_count(db, like: schemas.LikeCreate):
    db_seed = db.query(models.Seed).filter(
        models.Seed.id == like.seed_id).first()
    db_seed.like_count = db.query(models.Like).filter(
        models.Like.seed_id == like.seed_id,
        models.Like.is_like == True
    ).count()
    db.add(db_seed)
    db.commit()

# def get_dislikes(db: Session, seed_name: str):
#     seed_id = db.query(models.Seed).filter(
#         models.Seed.seed_name == seed_name).first().id
#     return db.query(models.Dislike).filter(models.Dislike.seed_id == seed_id).all()


# def create_dislike(db: Session, dislike: schemas.DislikesCreate):
#     db_dislike = models.Dislike(**dislike.dict())
#     db.add(db_dislike)
#     db.commit()
#     db.refresh(db_dislike)
#     return db_dislike


# def delete_dislike(db: Session, dislike: schemas.DislikesCreate):
#     db_dislike = db.query(models.Dislike).filter(
#         models.Dislike.user_id == dislike.user_id).filter(
#         models.Dislike.seed_id == dislike.seed_id).first()
#     db.delete(db_dislike)
#     db.commit()
#     return db_dislike
