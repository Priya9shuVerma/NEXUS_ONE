from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.database import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("iam_roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("iam_permissions.id", ondelete="CASCADE"), primary_key=True),
)


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("iam_roles.id", ondelete="CASCADE"), primary_key=True),
)


class IAMRole(Base):
    __tablename__ = "iam_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    permissions = relationship(
        "IAMPermission",
        secondary=role_permissions,
        back_populates="roles",
    )


class IAMPermission(Base):
    __tablename__ = "iam_permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    roles = relationship(
        "IAMRole",
        secondary=role_permissions,
        back_populates="permissions",
    )


class JITAccessRequest(Base):
    __tablename__ = "jit_access_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("iam_roles.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(1000), nullable=False)
    status = Column(String(30), default="pending", nullable=False)
    expires_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
