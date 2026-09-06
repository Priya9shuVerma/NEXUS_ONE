from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    resource: str,
    status: str = "SUCCESS",
    details: str | None = None,
    username: str | None = None,
    target: str | None = None,
    severity: str = "INFO",
    ip_address: str | None = None,
    user_agent: str | None = None,
):
    log = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        target=target or resource,
        status=status,
        severity=severity,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
