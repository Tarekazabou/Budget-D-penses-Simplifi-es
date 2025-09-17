from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Base de données
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/budget_app"
    
    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 heures
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Debug
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()