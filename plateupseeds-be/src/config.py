from pydantic import BaseSettings
from os import environ
env_file = environ.get('ENV_FILE', '.env')

class Settings(BaseSettings):
    DB_URL: str
    ENABLE_DOCS: bool

    class Config:
        env_file = env_file

settings = Settings()
