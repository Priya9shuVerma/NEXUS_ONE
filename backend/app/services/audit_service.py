from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


logger = logging.getLogger("nexus_one.audit")


# ============================================================
# SECURITY EVENT CLASSIFICATION
# ============================================================

HIGH_RISK_ACTIONS = {
    "LOGIN_FAILED",
    "ACCESS_DENIED",
    "TOKEN_REVOKED",
    "PASSWORD_CHANGED",
    "ADMIN_ACTION",
    "USER_DELETED",
}

WARNING_ACTIONS = {
    "LOGIN_FAILED",
    "ACCESS_DENIED",
    "TOKEN_REVOKED",
}

SUCCESS_ACTIONS = {
    "REGISTER",
    "LOGIN_SUCCESS",
    "LOGOUT",
    "PROFILE_UPDATE",
    "PASSWORD_CHANGED",
}


def _get_default_severity(action: str) -> str:
    """
    Determine security severity from the event type.
    """

    action = action.upper()

    if action in HIGH_RISK_ACTIONS:
        return "HIGH"

    if action in WARNING_ACTIONS:
        return "WARNING"

    return "INFO"


def _get_default_status(action: str) -> str:
    """
    Determine event status from the event type.
    """

    action = action.upper()

    if action in {"LOGIN_FAILED", "ACCESS_DENIED"}:
        return "FAILED"

    return "SUCCESS"


def _serialize_details(details: Any) -> str | None:
    """
    Safely convert optional audit details to JSON.

    Secrets must never be passed through this field.
    """

    if details is None:
        return None

    if isinstance(details, str):
        return details

    try:
        return json.dumps(
            details,
            ensure_ascii=False,
            default=str,
        )
    except Exception:
        return str(details)


# ============================================================
# SAVE AUDIT EVENT
# ============================================================

def save_audit_log(
    db: Session,
    user_id: int | None,
    username: str | None,
    action: str,
    target: str | None = None,
    ip_address: str | None = None,
    status: str | None = None,
    severity: str | None = None,
    user_agent: str | None = None,
    details: Any = None,
):
    """
    Store a security/activity event.

    Existing calls such as:

        save_audit_log(
            db=db,
            user_id=user.id,
            username=user.username,
            action="LOGIN_SUCCESS",
            target="AUTH",
            ip_address=request.client.host,
        )

    remain fully compatible.

    IMPORTANT:
    Never pass passwords, JWTs, refresh tokens, API keys,
    authorization headers, or other secrets in `details`.
    """

    action = action.upper().strip()

    if not action:
        raise ValueError("Audit action must not be empty")

    final_status = (
        status.upper().strip()
        if status
        else _get_default_status(action)
    )

    final_severity = (
        severity.upper().strip()
        if severity
        else _get_default_severity(action)
    )

    serialized_details = _serialize_details(details)

    log = AuditLog(
        user_id=user_id,
        username=username,
        action=action,
        target=target,
        status=final_status,
        severity=final_severity,
        ip_address=ip_address,
        user_agent=user_agent,
        details=serialized_details,
    )

    try:
        db.add(log)
        db.commit()
        db.refresh(log)

    except Exception:
        db.rollback()

        logger.exception(
            "Failed to save audit event | action=%s user_id=%s",
            action,
            user_id,
        )

        raise

    return log


# ============================================================
# SECURITY EVENT HELPERS
# ============================================================

def save_security_event(
    db: Session,
    action: str,
    *,
    user_id: int | None = None,
    username: str | None = None,
    target: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    status: str = "SUCCESS",
    severity: str = "INFO",
    details: Any = None,
):
    """
    Explicit security-event helper.

    Useful for future cybersecurity modules such as:
    - suspicious login detection
    - brute-force detection
    - admin security events
    - token revocation
    - unauthorized access
    """

    return save_audit_log(
        db=db,
        user_id=user_id,
        username=username,
        action=action,
        target=target,
        ip_address=ip_address,
        status=status,
        severity=severity,
        user_agent=user_agent,
        details=details,
    )


# ============================================================
# FAILED SECURITY EVENT
# ============================================================

def save_failed_security_event(
    db: Session,
    action: str,
    *,
    user_id: int | None = None,
    username: str | None = None,
    target: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    severity: str = "WARNING",
    details: Any = None,
):
    """
    Convenience helper for failed security operations.
    """

    return save_audit_log(
        db=db,
        user_id=user_id,
        username=username,
        action=action,
        target=target,
        ip_address=ip_address,
        status="FAILED",
        severity=severity,
        user_agent=user_agent,
        details=details,
    )
