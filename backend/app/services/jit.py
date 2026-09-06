from datetime import datetime

from sqlalchemy.orm import Session

from app.models.iam import JITAccessRequest, user_roles


def expire_jit_access(db: Session) -> int:
    now = datetime.utcnow()

    expired_requests = (
        db.query(JITAccessRequest)
        .filter(
            JITAccessRequest.status == "approved",
            JITAccessRequest.expires_at.isnot(None),
            JITAccessRequest.expires_at <= now,
        )
        .all()
    )

    count = 0

    for request in expired_requests:
        db.execute(
            user_roles.delete().where(
                user_roles.c.user_id == request.user_id,
                user_roles.c.role_id == request.role_id,
            )
        )

        request.status = "expired"
        count += 1

    if count:
        db.commit()

    return count


def has_active_jit_access(
    db: Session,
    user_id: int,
    role_id: int,
) -> bool:
    now = datetime.utcnow()

    request = (
        db.query(JITAccessRequest)
        .filter(
            JITAccessRequest.user_id == user_id,
            JITAccessRequest.role_id == role_id,
            JITAccessRequest.status == "approved",
            JITAccessRequest.expires_at.isnot(None),
            JITAccessRequest.expires_at > now,
        )
        .first()
    )

    return request is not None
