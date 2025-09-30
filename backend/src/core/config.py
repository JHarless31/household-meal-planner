"""
Application Configuration
Loads settings from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Household Meal Planning System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "household_db"
    DB_USER: str = "household_app"
    DB_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    SESSION_SECRET: str

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://meal-planner.local",
        "https://meal-planner.local"
    ]

    # Trusted Hosts
    ALLOWED_HOSTS: List[str] = ["*"]  # In production, specify actual hosts

    # Recipe Scraping
    SCRAPER_USER_AGENT: str = "HouseholdMealPlanner/1.0 (+http://meal-planner.local/about)"
    SCRAPER_RATE_LIMIT: int = 5  # seconds between requests per domain
    SCRAPER_TIMEOUT: int = 10  # seconds

    # File Upload
    MAX_FILE_SIZE: int = 5242880  # 5MB in bytes
    UPLOAD_PATH: str = "/app/uploads"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
