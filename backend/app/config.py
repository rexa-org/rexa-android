from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    S3_BUCKET: str = ""
    S3_KEY: str = ""
    S3_SECRET: str = ""
    ADMIN_EMAIL: str = "admin@rex.com"
    SECRET_KEY: str = "supersecret"

    class Config:
        env_file = ".env"

settings = Settings()
