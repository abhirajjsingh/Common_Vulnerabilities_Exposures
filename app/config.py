from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    COLLECTION_NAME: str
    API_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()