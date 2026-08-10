from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.blacklist_token import BlacklistToken
from app.core.jwt import verify_access_token
from app.core.security import sha256_hex


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    # avoid logging or printing the token

    # ---------------- BLACKLIST CHECK ---------------- #

    # compute token hash and prefer hashed lookup
    try:
        token_hash = sha256_hex(token)
    except Exception:
        token_hash = None

    blacklisted = None
    if token_hash:
        blacklisted = db.query(BlacklistToken).filter(
            BlacklistToken.token_hash == token_hash
        ).first()

    # legacy plaintext fallback
    if not blacklisted:
        blacklisted = db.query(BlacklistToken).filter(
            BlacklistToken.token == token
        ).first()

        # migrate legacy row to hashed storage (best-effort)
        if blacklisted and not blacklisted.token_hash:
            try:
                placeholder = f"removed_{__import__('uuid').uuid4().hex}"
                blacklisted.token_hash = sha256_hex(token)
                blacklisted.token = placeholder
                db.add(blacklisted)
                db.commit()
            except Exception:
                db.rollback()

    if blacklisted:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked. Please login again."
        )

    # ---------------- JWT VERIFY ---------------- #

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # ---------------- USER CHECK ---------------- #

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ---------------- ADMIN ONLY ---------------- #

def get_current_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user