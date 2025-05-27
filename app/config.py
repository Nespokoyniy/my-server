from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    IP_ADDRESS: str
    DB_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    REFRESH_SECRET_KEY: str
    REFRESH_ALGORITHM: str
    
    class Config:
        env_file = ".env"

settings = Settings()