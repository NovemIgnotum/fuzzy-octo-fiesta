from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv
import os 

load_dotenv()

class Settings(BaseSettings):
    # Paramètre de connexion mongoDB
    mongodb_url: str = os.getenv("MONGODB_URL") or "default_url"
    mongodb_database: str = os.getenv("MONGODB_DATABASE") or "default_db"
    
    # Paramètre des pools de mongoDB
    mongodb_min_pool_size: int = 10
    mongodb_max_pool_size: int = 100

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
    
    