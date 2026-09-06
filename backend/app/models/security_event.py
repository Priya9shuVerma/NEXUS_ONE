from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text

from app.db.database import Base


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    username = Column(
        String,
        nullable=True,
        index=True
    )

    event_type = Column(
        String,
        nullable=False,
        index=True
    )

    severity = Column(
        String,
        nullable=False,
        default="INFO",
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    ip_address = Column(
        String,
        nullable=True,
        index=True
    )

    user_agent = Column(
        String,
        nullable=True
    )

    endpoint = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
