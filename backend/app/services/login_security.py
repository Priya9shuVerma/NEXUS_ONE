from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.security_event import SecurityEvent


FAILED_LOGIN_WINDOW_MINUTES = 15
MAX_FAILED_LOGINS = 5


def record_failed_login(
    db: Session,
    username: str | None,
    ip_address: str | None,
    endpoint: str | None = None,
    user_agent: str | None = None,
    user_id: int | None = None,
):
    event = SecurityEvent(
        user_id=user_id,
        username=username,
        event_type="LOGIN_FAILED",
        severity="WARNING",
        description="Failed login attempt",
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def count_recent_failed_logins(
    db: Session,
    username: str | None = None,
    ip_address: str | None = None,
) -> int:

    since = datetime.utcnow() - timedelta(
        minutes=FAILED_LOGIN_WINDOW_MINUTES
    )

    query = db.query(
        func.count(SecurityEvent.id)
    ).filter(
        SecurityEvent.event_type == "LOGIN_FAILED",
        SecurityEvent.created_at >= since,
    )

    if username:
        query = query.filter(
            SecurityEvent.username == username
        )

    if ip_address:
        query = query.filter(
            SecurityEvent.ip_address == ip_address
        )

    return query.scalar() or 0


def is_suspicious_login(
    db: Session,
    username: str | None = None,
    ip_address: str | None = None,
) -> bool:

    failed_attempts = count_recent_failed_logins(
        db=db,
        username=username,
        ip_address=ip_address,
    )

    return failed_attempts >= MAX_FAILED_LOGINS


def record_suspicious_login(
    db: Session,
    username: str | None = None,
    ip_address: str | None = None,
    user_id: int | None = None,
    endpoint: str | None = None,
    user_agent: str | None = None,
):

    event = SecurityEvent(
        user_id=user_id,
        username=username,
        event_type="SUSPICIOUS_LOGIN",
        severity="HIGH",
        description=(
            "Multiple failed login attempts detected"
        ),
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
