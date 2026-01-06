from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Arete"
    debug: bool = True
    
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # LLM
    llm_provider: str = "claude"
    claude_api_key: str
    
    # File limits
    max_file_size_mb: int = 10
    allowed_file_types: List[str] = ["pdf", "docx", "txt"]
    
    class Config:
        env_file = ".env"

settings = Settings()
