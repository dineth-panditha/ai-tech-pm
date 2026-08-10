from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Project Manager API"
    VERSION: str = "1.0.0"

    SUPABASE_URL: str
    SUPABASE_KEY: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        #extra = "ignore"

settings = Settings()






    
    