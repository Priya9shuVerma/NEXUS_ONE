from sqlalchemy.orm import Session

from app.models.security_event import SecurityEvent


def record_security_event(
    db: Session,
    event_type: str,
    severity: str = "INFO",
    description: str | None = None,
    user_id: int | None = None,
    username: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    endpoint: str | None = None,
):
    event = SecurityEvent(
        user_id=user_id,
        username=username,
        event_type=event_type,
        severity=severity,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
