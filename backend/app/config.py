from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET: str
    
    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    
    # AWS S3 (optional)
    S3_BUCKET: str = ""
    S3_KEY: str = ""
    S3_SECRET: str = ""
    S3_REGION: str = "us-east-1"
    
    # Application
    ADMIN_EMAIL: str = "admin@rex.com"
    SECRET_KEY: str = "supersecret"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081", "exp://localhost:8081"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
