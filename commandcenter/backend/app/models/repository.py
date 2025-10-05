"""
Repository model for tracking GitHub repositories
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Repository(Base):
    """GitHub repository tracking"""

    __tablename__ = "repositories"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Repository identification
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)

    # GitHub metadata
    github_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    clone_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    default_branch: Mapped[str] = mapped_column(String(255), default="main")

    # Access control
    access_token: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_private: Mapped[bool] = mapped_column(default=False)

    # Last sync information
    last_commit_sha: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_commit_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_commit_author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_commit_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Repository stats
    stars: Mapped[int] = mapped_column(default=0)
    forks: Mapped[int] = mapped_column(default=0)
    language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Additional metadata (JSON field for flexibility)
    # Note: 'metadata_' to avoid conflict with SQLAlchemy's reserved 'metadata'
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    research_tasks: Mapped[list["ResearchTask"]] = relationship(
        "ResearchTask",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Repository(id={self.id}, full_name='{self.full_name}')>"
