from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User


router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)


@router.get("/logs")
def get_audit_logs(
    action: str | None = None,
    status: str | None = None,
    severity: str | None = None,
    user_id: int | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)

    if status:
        query = query.filter(AuditLog.status == status)

    if severity:
        query = query.filter(AuditLog.severity == severity)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    return (
        query
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/stats")
def audit_stats(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    total = db.query(AuditLog).count()

    success = (
        db.query(AuditLog)
        .filter(AuditLog.status == "SUCCESS")
        .count()
    )

    failed = (
        db.query(AuditLog)
        .filter(AuditLog.status == "FAILED")
        .count()
    )

    denied = (
        db.query(AuditLog)
        .filter(AuditLog.status == "DENIED")
        .count()
    )

    critical = (
        db.query(AuditLog)
        .filter(AuditLog.severity == "CRITICAL")
        .count()
    )

    high = (
        db.query(AuditLog)
        .filter(AuditLog.severity == "HIGH")
        .count()
    )

    return {
        "total": total,
        "success": success,
        "failed": failed,
        "denied": denied,
        "critical": critical,
        "high": high,
    }
