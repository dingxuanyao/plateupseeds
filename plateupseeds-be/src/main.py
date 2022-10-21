from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from authlib.integrations.starlette_client import OAuthError
from starlette.responses import HTMLResponse, RedirectResponse, Response


from . import crud, models, schemas
from .database import SessionLocal, engine

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from .config import settings


config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# alembic_config = AlembicConfig("alembic.ini")
# alembic_config.set_main_option("sqlalchemy.url", settings.DB_URL)
# command.upgrade(alembic_config, 'head')


app = FastAPI(
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
)

app.add_middleware(SessionMiddleware, secret_key="secret-string")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/users/", response_model=schemas.User)
def get_user(email: str = "", user_id: int = 0, db: Session = Depends(get_db)):
    if email and user_id:
        raise HTTPException(status_code=400, detail="You can only pass either email or user_id")
    if email:
        user = crud.get_user_by_email(db, email)
    if user_id:
        user = crud.get_user_by_id(db, user_id)
    if user:
        return user
    return crud.create_user(db=db, user=schemas.UserCreate(email=email))


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=schemas.UserCreate(email=user.email))

@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/seeds/{seed_id}", response_model=schemas.Seed)
def read_seeds(seed_id: str, db: Session = Depends(get_db)):
    seed = crud.get_seed(db, seed_id=seed_id)
    if seed is None:
        raise HTTPException(status_code=404, detail="Seed not found")
    return seed


@app.get("/seeds_by_type/{seed_type}", response_model=list[int])
def read_seeds(seed_type: str, skip: int = 0, limit: int = 100, random: bool = False, db: Session = Depends(get_db)):
    seeds = crud.get_seeds(db, seed_type=seed_type,
                           skip=skip, limit=limit, random=random)
    seed_ids = [seed.id for seed in seeds]
    return seed_ids


@app.get("/count_seeds_by_type/{seed_type}", response_model=int)
def read_seeds(seed_type: str, db: Session = Depends(get_db)):
    count = crud.get_seeds_count(db, seed_type=seed_type)
    return count


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


@app.route('/login')
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return user

    return RedirectResponse(url='/')


@app.get("/db_health")
def db_health_check():
    db_status = crud.db_health_check(db=SessionLocal())
    if db_status:
        return Response(status_code=200)
    else:
        return HTTPException(status_code=500, detail="Cannot connect to database")


@app.get("/comments/{seed_id}", response_model=list[schemas.Comment])
def get_comments(seed_id: str, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, seed_id=seed_id)
    return comments


@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment=comment)

@app.get("/")
async def main():
    return {"message": "Hello World"}
