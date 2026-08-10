from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

from app.db.database import Base


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    token = Column(
        String,
        unique=True,
        nullable=True
    )

    # New token hash column for storing SHA-256(token) — nullable for
    # backward compatibility during migration.
    token_hash = Column(
        String,
        nullable=True,
        index=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(days=7)
    )