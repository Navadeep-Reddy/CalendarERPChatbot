"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Gemini Configuration
    google_api_key: str = ""
    
    # Application Settings
    app_name: str = "Calendar ERP Chatbot"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # LLM Settings
    llm_model: str = "gemini-2.5-flash"
    llm_temperature: float = 0.7
    max_tokens: int = 500
    
    # Vector Store Settings
    vector_db_path: str = "./data/vectorstore"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
