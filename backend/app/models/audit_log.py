from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Index,
)

from app.db.database import Base


class AuditLog(Base):
    """
    Security and activity audit log.

    Stores security-relevant events such as:
    - REGISTER
    - LOGIN_SUCCESS
    - LOGIN_FAILED
    - LOGOUT
    - PASSWORD_CHANGED
    - PROFILE_UPDATE
    - ADMIN_ACTION
    - TOKEN_REVOKED
    - ACCESS_DENIED
    """

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        nullable=True,
        index=True,
    )

    username = Column(
        String(255),
        nullable=True,
        index=True,
    )

    action = Column(
        String(100),
        nullable=False,
        index=True,
    )

    target = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="SUCCESS",
        index=True,
    )

    severity = Column(
        String(20),
        nullable=False,
        default="INFO",
        index=True,
    )

    ip_address = Column(
        String(100),
        nullable=True,
        index=True,
    )

    user_agent = Column(
        String(500),
        nullable=True,
    )

    details = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )


# Useful indexes for security monitoring and admin dashboards.
Index(
    "ix_audit_logs_action_created_at",
    AuditLog.action,
    AuditLog.created_at,
)

Index(
    "ix_audit_logs_user_created_at",
    AuditLog.user_id,
    AuditLog.created_at,
)

Index(
    "ix_audit_logs_ip_created_at",
    AuditLog.ip_address,
    AuditLog.created_at,
)
