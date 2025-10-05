"""
Application configuration using Pydantic Settings
Loads configuration from environment variables and .env file
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Command Center API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./commandcenter.db",
        description="Database connection URL"
    )

    # PostgreSQL settings (for production)
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    postgres_db: Optional[str] = None

    # GitHub Integration
    github_token: Optional[str] = None
    github_default_org: Optional[str] = None

    # RAG/Knowledge Base
    knowledge_base_path: str = Field(
        default="./docs/knowledge-base/chromadb",
        description="Path to ChromaDB vector store"
    )
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Security
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )

    # API Settings
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_postgres_url(self) -> str:
        """Construct PostgreSQL URL from components"""
        if all([self.postgres_user, self.postgres_password, self.postgres_host, self.postgres_db]):
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        return self.database_url


# Global settings instance
settings = Settings()
