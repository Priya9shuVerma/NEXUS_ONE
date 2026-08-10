from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(String, unique=True, nullable=True)

    # New token_hash column for storing SHA-256(token) — nullable for
    # backward compatibility during migration.
    token_hash = Column(
        String,
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )