"""
Configuration management for DayPilot backend application.

Uses pydantic-settings for environment-based configuration with type validation.
"""

from pydantic import Field, field_validator
from typing import List, Optional
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""
    
    # Application settings
    DEBUG: bool = Field(default=True, description="Enable debug mode")
    APP_NAME: str = Field(default="DayPilot AI Scheduler", description="Application name")
    VERSION: str = Field(default="1.0.0", description="Application version")
    
    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite:///./daypilot.db",
        description="Database connection URL"
    )
    
    # Security settings
    SECRET_KEY: str = Field(
        default="daypilot-dev-secret-key-change-in-production",
        description="Secret key for JWT tokens and encryption"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1", "0.0.0.0"],
        description="Allowed host headers"
    )
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",  # Vite dev server
        ],
        description="Allowed CORS origins"
    )
    
    # AI/ML Service Configuration  
    GEMINI_API_KEY: Optional[str] = Field(
        default=None,
        description="Google Gemini API key for LLM services"
    )
    GEMINI_MODEL: str = Field(
        default="gemini-pro",
        description="Gemini model for task parsing"
    )
    
    # Redis settings (for caching and sessions)
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL for caching"
    )
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Performance settings
    TASK_PARSING_TIMEOUT: int = Field(
        default=10,
        description="Timeout in seconds for task parsing operations"
    )
    SCHEDULE_GENERATION_TIMEOUT: int = Field(
        default=15,
        description="Timeout in seconds for schedule generation"
    )
    
    # ML Model settings
    ML_MODEL_PATH: str = Field(
        default="./models",
        description="Path to ML model files"
    )
    ENABLE_ML_TRAINING: bool = Field(
        default=True,
        description="Enable incremental ML model training"
    )
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v):
        """Ensure database directory exists for SQLite."""
        if v.startswith("sqlite:///"):
            db_path = Path(v.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return v
    
    @field_validator("ML_MODEL_PATH")
    @classmethod
    def validate_model_path(cls, v):
        """Ensure ML model directory exists."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings (useful for testing)."""
    global _settings
    _settings = None
    return get_settings()