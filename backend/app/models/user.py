from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    hashed_password = Column(
        String,
        nullable=False
    )


    # -------- Profile Details --------

    full_name = Column(
        String,
        nullable=True
    )


    phone = Column(
        String,
        nullable=True
    )


    bio = Column(
        String,
        nullable=True
    )


    profile_image = Column(
        String,
        nullable=True
    )


    # -------- Role Management --------

    role = Column(
        String,
        default="user",
        nullable=False
    )


    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )