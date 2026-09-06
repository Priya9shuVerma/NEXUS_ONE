from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.database import Base


class CloudAccount(Base):
    __tablename__ = "cloud_accounts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, index=True)

    provider = Column(String(50), nullable=False, index=True)

    account_identifier = Column(
        String(150),
        nullable=False,
        index=True,
    )

    region = Column(String(100), nullable=True)

    status = Column(
        String(30),
        default="active",
        nullable=False,
    )

    description = Column(String(500), nullable=True)

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
