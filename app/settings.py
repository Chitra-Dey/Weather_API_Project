from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_URL:str
    JWT_SECRET:str
    JWT_ALGO:str
    PAGE_SIZE:int
    API_KEY:str
    model_config = SettingsConfigDict(env_file=".env")
settings=Settings()
