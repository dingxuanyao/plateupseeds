from ast import Str
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas

from datetime import datetime, timezone


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).filter(
        models.User.email == user.email).first()
    db_user.anonymous_name = user.anonymous_name
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_seeds(db: Session, seed_type: Str,  skip: int = 0, limit: int = 100, random: bool = False, sort_by_likes: bool = False, seed_theme: str = 'all'):
    seeds = []
    if seed_theme != 'all':
        seeds = db.query(models.Seed).filter(
            models.Seed.seed_type == seed_type).filter(
            models.Seed.seed_theme == seed_theme)
    else:
        seeds = db.query(models.Seed).filter(
            models.Seed.seed_type == seed_type)
    if random:
        seeds_sorted = seeds.order_by(func.random())
        # order_by = func.random()
    elif sort_by_likes:
        seeds_sorted = seeds.order_by(models.Seed.like_count.desc()).order_by(models.Seed.comment_count.desc())
    else:
        seeds_sorted = seeds.order_by(models.Seed.comment_count.desc()).order_by(models.Seed.like_count.desc())
    # sorted by number of likes
    return seeds_sorted.offset(skip).limit(limit).all()
    seeds = db.query(models.Seed).filter(
        models.Seed.seed_type == seed_type).order_by(
        order_by).offset(skip).limit(limit).all()
    return seeds


def get_seeds_count(db: Session, seed_type: Str):
    return db.query(models.Seed).filter(
        models.Seed.seed_type == seed_type).count()


def get_seed(db: Session, seed_id: str,):
    seed = db.query(models.Seed).filter(models.Seed.id == seed_id).first()
    return seed


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

    return db_like


def delete_like(db: Session, like: schemas.LikeCreate):
    db_like = db.query(models.Like).filter(
        models.Like.user_id == like.user_id).filter(
        models.Like.seed_id == like.seed_id).first()
    db.delete(db_like)
    db.commit()
    return db_like


def get_comments(db: Session, seed_id: int):
    return db.query(models.Comment).filter(models.Comment.seed_id == seed_id).order_by(models.Comment.created_time.desc()).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    created_time = datetime.utcnow()
    db_comment = models.Comment(**comment.dict(), created_time=created_time)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def db_health_check(db: Session):
    # check if can connect to db
    try:
        db.execute("SELECT 1")
        return True
    except:
        return False
