from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def save_audit_log(
    db: Session,
    user_id: int | None,
    username: str | None,
    action: str,
    target: str | None = None,
    ip_address: str | None = None
):

    log = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        target=target,
        ip_address=ip_address
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log