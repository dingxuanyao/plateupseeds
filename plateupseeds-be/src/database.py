from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import databases
from .config import settings

DATABASE_URL = settings.DB_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
)
# database = databases.Database(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
