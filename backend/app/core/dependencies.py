from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.blacklist_token import BlacklistToken
from app.core.jwt import verify_access_token
from app.core.security import sha256_hex

security = HTTPBearer()


# ============================================================
# CURRENT AUTHENTICATED USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # --------------------------------------------------------
    # BLACKLIST / TOKEN REVOCATION CHECK
    # --------------------------------------------------------

    try:
        token_hash = sha256_hex(token)
    except Exception:
        token_hash = None

    blacklisted = None

    # Prefer hashed token lookup
    if token_hash:
        blacklisted = (
            db.query(BlacklistToken)
            .filter(
                BlacklistToken.token_hash == token_hash
            )
            .first()
        )

    # Legacy plaintext fallback
    if not blacklisted:
        blacklisted = (
            db.query(BlacklistToken)
            .filter(
                BlacklistToken.token == token
            )
            .first()
        )

        # Migrate legacy plaintext token to hashed storage
        if blacklisted and not blacklisted.token_hash:
            try:
                import uuid

                blacklisted.token_hash = token_hash
                blacklisted.token = f"removed_{uuid.uuid4().hex}"

                db.add(blacklisted)
                db.commit()

            except Exception:
                db.rollback()

    # Token has been revoked
    if blacklisted:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked. Please login again."
        )

    # --------------------------------------------------------
    # JWT VERIFICATION
    # --------------------------------------------------------

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token"
        )

    # --------------------------------------------------------
    # TOKEN TYPE CHECK
    # --------------------------------------------------------

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    # --------------------------------------------------------
    # USER ID VALIDATION
    # --------------------------------------------------------

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    # --------------------------------------------------------
    # USER LOOKUP
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # --------------------------------------------------------
    # ACCOUNT STATUS CHECK
    # --------------------------------------------------------

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    return user


# ============================================================
# ADMIN ONLY
# ============================================================

def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user
