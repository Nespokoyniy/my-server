from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    IP_ADDRESS: str
    DB_NAME: str
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()