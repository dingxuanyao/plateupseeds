from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/seeds/{seed_name}", response_model=schemas.Seed)
def read_seeds(seed_name: str, db: Session = Depends(get_db)):
    seed = crud.get_seed(db, seed_name=seed_name)
    if seed is None:
        raise HTTPException(status_code=404, detail="Seed not found")
    return seed


@app.get("/seeds_by_type/{seed_type}", response_model=list[schemas.Seed])
def read_seeds(seed_type: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    seed = crud.get_seeds(db, seed_type=seed_type, skip=skip, limit=limit)
    return seed


@app.post("/seeds/", response_model=schemas.Seed)
def create_seed(seed: schemas.SeedCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Seed).filter(
        models.Seed.seed_name == seed.seed_name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Seed already exists")
    allowed_seed_types = ["large", "medium", "small", "default"]
    if seed.seed_type not in allowed_seed_types:
        raise HTTPException(status_code=400, detail="Seed size not allowed")
    return crud.create_seed(db, seed=seed)


@app.get("/likes/{seed_name}", response_model=list[schemas.Like])
def get_likes(seed_name: str, db: Session = Depends(get_db)):
    likes = crud.get_likes(db, seed_name=seed_name)
    return likes


@app.post("/likes/", response_model=schemas.Like)
def upsert_like(like: schemas.LikeCreate, db: Session = Depends(get_db)):
    return crud.upsert_like(db, like=like)


@app.delete("/likes/", response_model=schemas.Like)
def delete_like(like: schemas.LikeDelete, db: Session = Depends(get_db)):
    return crud.delete_like(db, like=like)


# @app.get("/dislikes/{seed_name}", response_model=list[schemas.Dislikes])
# def get_dislikes(seed_name: str, db: Session = Depends(get_db)):
#     dislikes = crud.get_dislikes(db, seed_name=seed_name)
#     return dislikes


# @app.post("/dislikes/", response_model=schemas.DislikesCreate)
# def create_dislike(dislike: schemas.LikesCreate, db: Session = Depends(get_db)):
#     return crud.create_dislike(db, dislike=dislike)


# @app.delete("/dislikes/", response_model=schemas.Dislikes)
# def delete_dislike(dislike: schemas.LikesCreate, db: Session = Depends(get_db)):
#     return crud.delete_dislike(db, dislike=dislike)


@app.get("/")
async def main():
    return {"message": "Hello World"}
