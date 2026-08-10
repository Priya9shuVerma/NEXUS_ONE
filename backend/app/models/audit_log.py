from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=True
    )

    username = Column(
        String,
        nullable=True
    )

    action = Column(
        String,
        nullable=False
    )

    target = Column(
        String,
        nullable=True
    )

    ip_address = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )