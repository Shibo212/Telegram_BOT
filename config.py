from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "7419683872:AAGzltIqObWB34vqXhNC2LlPnstH8GJ_d5M"
    DATABASE_URL: str = "sqlite:///dutch_learning.db"
    GOOGLE_CLOUD_PROJECT: str = "dutch-learning-bot"
    GOOGLE_APPLICATION_CREDENTIALS: str = "credentials.json"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()