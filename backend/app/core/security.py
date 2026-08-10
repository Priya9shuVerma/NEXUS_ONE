from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):

    password = password.encode("utf-8")[:72].decode(
        "utf-8",
        errors="ignore"
    )

    return pwd_context.hash(password)



def verify_password(
    plain_password: str,
    hashed_password: str
):

    plain_password = plain_password.encode("utf-8")[:72].decode(
        "utf-8",
        errors="ignore"
    )

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ---------------- TOKEN HASH HELPER ---------------- #
import hashlib

def sha256_hex(token: str) -> str:
    """
    Compute SHA-256 hex digest of the UTF-8 encoded token string.
    Do NOT log or print the token.
    """
    if token is None:
        raise ValueError("token must not be None")
    token_bytes = token.encode("utf-8")
    return hashlib.sha256(token_bytes).hexdigest()
