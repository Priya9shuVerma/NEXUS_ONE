"""
NEXUS ONE - Password Security Policy

Centralized password validation rules.
"""

import re


MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Returns:
        (True, "") when valid.
        (False, reason) when invalid.
    """

    if not isinstance(password, str):
        return False, "Password must be a string"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must contain at least {MIN_PASSWORD_LENGTH} characters"

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must not exceed {MAX_PASSWORD_LENGTH} characters"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password must contain at least one special character"

    return True, ""


def is_strong_password(password: str) -> bool:
    """
    Convenience helper for password validation.
    """
    valid, _ = validate_password(password)
    return valid
