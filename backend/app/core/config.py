from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CV Generator API"
    api_v1_str: str = "/api/v1"
    
    # Database
    database_url: str = "sqlite:///./cv_generator.db"
    
    # CORS
    allowed_hosts: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:5500", "http://localhost:5500"]
    
    # Google API Key for Gemini
    google_api_key: str
    
    model_config = SettingsConfigDict(
        env_file="backend\.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings():
    return Settings()
