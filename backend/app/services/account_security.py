from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.user import User


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def is_account_locked(user: User) -> bool:
    if not user.locked_until:
        return False

    if user.locked_until > datetime.utcnow():
        return True

    # Lock expired
    user.locked_until = None
    user.failed_login_attempts = 0

    return False


def register_failed_attempt(
    db: Session,
    user: User,
):
    user.failed_login_attempts = (
        (user.failed_login_attempts or 0) + 1
    )

    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        user.locked_until = (
            datetime.utcnow()
            + timedelta(minutes=LOCKOUT_MINUTES)
        )

    db.commit()
    db.refresh(user)

    return user


def register_successful_login(
    db: Session,
    user: User,
    ip_address: str | None = None,
):
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = ip_address

    db.commit()
    db.refresh(user)

    return user
