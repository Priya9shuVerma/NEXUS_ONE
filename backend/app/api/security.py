from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.security_event import SecurityEvent
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/security",
    tags=["Cybersecurity"]
)


@router.get("/")
async def security_home():
    return {
        "message": "Cybersecurity API Working"
    }


@router.get("/events")
async def get_security_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    events = (
        db.query(SecurityEvent)
        .order_by(SecurityEvent.created_at.desc())
        .limit(100)
        .all()
    )

    return events


@router.get("/events/critical")
async def get_critical_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    events = (
        db.query(SecurityEvent)
        .filter(SecurityEvent.severity == "CRITICAL")
        .order_by(SecurityEvent.created_at.desc())
        .limit(100)
        .all()
    )

    return events


@router.get("/events/high")
async def get_high_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    events = (
        db.query(SecurityEvent)
        .filter(SecurityEvent.severity == "HIGH")
        .order_by(SecurityEvent.created_at.desc())
        .limit(100)
        .all()
    )

    return events
from sqlalchemy import func
@router.get("/stats")
async def security_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    total_events = db.query(
        SecurityEvent
    ).count()

    critical_events = db.query(
        SecurityEvent
    ).filter(
        SecurityEvent.severity == "CRITICAL"
    ).count()

    high_events = db.query(
        SecurityEvent
    ).filter(
        SecurityEvent.severity == "HIGH"
    ).count()

    warning_events = db.query(
        SecurityEvent
    ).filter(
        SecurityEvent.severity == "WARNING"
    ).count()

    failed_logins = db.query(
        SecurityEvent
    ).filter(
        SecurityEvent.event_type == "LOGIN_FAILED"
    ).count()

    suspicious_logins = db.query(
        SecurityEvent
    ).filter(
        SecurityEvent.event_type == "SUSPICIOUS_LOGIN"
    ).count()

    return {
        "total_events": total_events,
        "critical_events": critical_events,
        "high_events": high_events,
        "warning_events": warning_events,
        "failed_logins": failed_logins,
        "suspicious_logins": suspicious_logins,
    }
