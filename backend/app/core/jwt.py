from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.core.config import settings


# Legacy secret handling moved to configuration. The setting is optional
# and when absent, legacy-token verification is disabled.
# Keep the legacy secret in Settings only if backwards compatibility is
# required; do NOT hard-code secrets in source.
# LEGACY_SECRET (optional) is read from app.core.config.settings.LEGACY_SECRET

# Primary secret and algorithm come from settings
# New tokens will be signed with settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# Access Token (Short Life)
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Refresh Token (Long Life)
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ---------------- ACCESS TOKEN ---------------- #

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    # Sign new tokens with the canonical secret from settings
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


# ---------------- REFRESH TOKEN ---------------- #

def create_refresh_token(data: dict, expires_delta=None):

    to_encode = data.copy()

    if expires_delta is None:
        expire = datetime.utcnow() + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    else:
        expire = datetime.utcnow() + expires_delta

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow().timestamp()
    })

    # Sign new tokens with the canonical secret from settings
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


# ---------------- VERIFY HELPERS ---------------- #

def _decode_with_secret(token: str, secret: str):
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_refresh_token(token: str):
    """
    Verify the refresh token. Try primary (settings.SECRET_KEY) first,
    then fallback to the legacy secret for compatibility.
    Returns the payload dict on success or None on failure.
    """

    # Try primary secret
    payload = _decode_with_secret(token, settings.SECRET_KEY)

    if payload is None:
        # Fallback to legacy secret only if configured in settings
        legacy = getattr(settings, 'LEGACY_SECRET', None)
        if legacy:
            payload = _decode_with_secret(token, legacy)

    if not payload:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload


def verify_access_token(token: str):
    """
    Verify an access token the same way as refresh tokens: try the
    canonical settings.SECRET_KEY first, then the LEGACY_SECRET.
    Returns payload dict on success, or None on failure.
    """

    payload = _decode_with_secret(token, settings.SECRET_KEY)

    if payload is None:
        # Fallback to legacy secret only if configured in settings
        legacy = getattr(settings, 'LEGACY_SECRET', None)
        if legacy:
            payload = _decode_with_secret(token, legacy)

    if not payload:
        return None

    if payload.get("type") != "access":
        return None

    return payload