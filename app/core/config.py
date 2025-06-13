from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./portfolio.db"
    secret_key: str = "dev-secret-key-change-in-production"
    alpha_vantage_api_key: Optional[str] = None
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()