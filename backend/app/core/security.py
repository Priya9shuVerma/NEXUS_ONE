from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
import hashlib


# ============================================================
# PASSWORD HASHING
# ============================================================

# Argon2 is preferred for new passwords.
# Bcrypt is retained for compatibility with existing users.
password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using the preferred Argon2 hasher.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against Argon2 or bcrypt hashes.
    """
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# TOKEN HASH HELPER
# ============================================================

def sha256_hex(token: str) -> str:
    """
    Compute SHA-256 hex digest of the UTF-8 encoded token string.
    Do NOT log or print the token.
    """
    if token is None:
        raise ValueError("token must not be None")

    token_bytes = token.encode("utf-8")
    return hashlib.sha256(token_bytes).hexdigest()
