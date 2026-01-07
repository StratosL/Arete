import logging

from pydantic_settings import BaseSettings

# Configure logging with hybrid dotted namespace pattern
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    allowed_file_types: list[str] = ["pdf", "docx", "txt"]

    class Config:
        env_file = ".env"

settings = Settings()

# Log configuration loaded
logger.info("application.config.loaded", extra={
    "app_name": settings.app_name,
    "debug": settings.debug,
    "max_file_size_mb": settings.max_file_size_mb
})
