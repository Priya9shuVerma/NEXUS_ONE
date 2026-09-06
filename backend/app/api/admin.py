from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.dependencies import get_current_admin
from app.services.audit_service import save_audit_log


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# ============================================================
# ADMIN HOME
# ============================================================

@router.get("/")
async def admin_home(
    current_admin: User = Depends(get_current_admin),
):
    return {
        "message": f"Welcome Admin {current_admin.username}",
        "role": current_admin.role,
    }


# ============================================================
# ADMIN STATS
# ============================================================

@router.get("/stats")
async def admin_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return {
        "total_users": db.query(User).count(),

        "active_users": (
            db.query(User)
            .filter(User.is_active == True)
            .count()
        ),

        "inactive_users": (
            db.query(User)
            .filter(User.is_active == False)
            .count()
        ),

        "admins": (
            db.query(User)
            .filter(User.role == "admin")
            .count()
        ),

        "audit_logs": db.query(AuditLog).count(),

        "failed_security_events": (
            db.query(AuditLog)
            .filter(AuditLog.status == "FAILED")
            .count()
        ),

        "high_severity_events": (
            db.query(AuditLog)
            .filter(AuditLog.severity == "HIGH")
            .count()
        ),
    }


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    latest_users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )

    latest_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "system": "NEXUS ONE",

        "statistics": {
            "total_users": db.query(User).count(),

            "active_users": (
                db.query(User)
                .filter(User.is_active == True)
                .count()
            ),

            "inactive_users": (
                db.query(User)
                .filter(User.is_active == False)
                .count()
            ),

            "admin_users": (
                db.query(User)
                .filter(User.role == "admin")
                .count()
            ),

            "total_audit_logs": db.query(AuditLog).count(),

            "failed_events": (
                db.query(AuditLog)
                .filter(AuditLog.status == "FAILED")
                .count()
            ),

            "high_severity_events": (
                db.query(AuditLog)
                .filter(AuditLog.severity == "HIGH")
                .count()
            ),
        },

        "latest_users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
            }
            for user in latest_users
        ],

        "latest_security_events": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "action": log.action,
                "target": log.target,
                "status": log.status,
                "severity": log.severity,
                "ip_address": log.ip_address,
                "created_at": log.created_at,
            }
            for log in latest_logs
        ],
    }


# ============================================================
# GET ALL USERS
# ============================================================

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    users = (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )

    return {
        "total_users": len(users),

        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
            }
            for user in users
        ],
    }


# ============================================================
# DISABLE USER
# ============================================================

@router.put("/disable-user/{user_id}")
async def disable_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot disable your own account",
        )

    if not user.is_active:
        return {
            "message": "User is already disabled",
            "user_id": user.id,
        }

    user.is_active = False

    db.commit()
    db.refresh(user)

    save_audit_log(
        db=db,
        user_id=current_admin.id,
        username=current_admin.username,
        action="ADMIN_ACTION",
        target=f"DISABLE_USER:{user.id}",
        ip_address=request.client.host,
        status="SUCCESS",
        severity="HIGH",
        details={
            "target_user_id": user.id,
            "target_username": user.username,
            "operation": "DISABLE_USER",
        },
    )

    return {
        "message": f"{user.username} disabled",
        "user_id": user.id,
        "is_active": user.is_active,
    }


# ============================================================
# ENABLE USER
# ============================================================

@router.put("/enable-user/{user_id}")
async def enable_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.is_active:
        return {
            "message": "User is already active",
            "user_id": user.id,
        }

    user.is_active = True

    db.commit()
    db.refresh(user)

    save_audit_log(
        db=db,
        user_id=current_admin.id,
        username=current_admin.username,
        action="ADMIN_ACTION",
        target=f"ENABLE_USER:{user.id}",
        ip_address=request.client.host,
        status="SUCCESS",
        severity="HIGH",
        details={
            "target_user_id": user.id,
            "target_username": user.username,
            "operation": "ENABLE_USER",
        },
    )

    return {
        "message": f"{user.username} enabled",
        "user_id": user.id,
        "is_active": user.is_active,
    }


# ============================================================
# MAKE ADMIN
# ============================================================

@router.put("/make-admin/{user_id}")
async def make_admin(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.role == "admin":
        return {
            "message": "User is already an Admin",
            "role": user.role,
        }

    user.role = "admin"

    db.commit()
    db.refresh(user)

    save_audit_log(
        db=db,
        user_id=current_admin.id,
        username=current_admin.username,
        action="ADMIN_ACTION",
        target=f"ROLE_CHANGE:{user.id}",
        ip_address=request.client.host,
        status="SUCCESS",
        severity="HIGH",
        details={
            "target_user_id": user.id,
            "target_username": user.username,
            "old_role": "user",
            "new_role": "admin",
            "operation": "PROMOTE_ADMIN",
        },
    )

    return {
        "message": f"{user.username} promoted to Admin",
        "role": user.role,
    }


# ============================================================
# MAKE USER
# ============================================================

@router.put("/make-user/{user_id}")
async def make_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own admin role",
        )

    if user.role == "user":
        return {
            "message": "User is already a normal User",
            "role": user.role,
        }

    user.role = "user"

    db.commit()
    db.refresh(user)

    save_audit_log(
        db=db,
        user_id=current_admin.id,
        username=current_admin.username,
        action="ADMIN_ACTION",
        target=f"ROLE_CHANGE:{user.id}",
        ip_address=request.client.host,
        status="SUCCESS",
        severity="HIGH",
        details={
            "target_user_id": user.id,
            "target_username": user.username,
            "old_role": "admin",
            "new_role": "user",
            "operation": "DEMOTE_ADMIN",
        },
    )

    return {
        "message": f"{user.username} changed to User",
        "role": user.role,
    }


# ============================================================
# DELETE USER
# ============================================================

@router.delete("/delete-user/{user_id}")
async def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account",
        )

    deleted_user_id = user.id
    deleted_username = user.username

    db.delete(user)
    db.commit()

    save_audit_log(
        db=db,
        user_id=current_admin.id,
        username=current_admin.username,
        action="ADMIN_ACTION",
        target=f"DELETE_USER:{deleted_user_id}",
        ip_address=request.client.host,
        status="SUCCESS",
        severity="HIGH",
        details={
            "target_user_id": deleted_user_id,
            "target_username": deleted_username,
            "operation": "DELETE_USER",
        },
    )

    return {
        "message": "User deleted successfully",
        "user_id": deleted_user_id,
    }


# ============================================================
# AUDIT LOGS
# ============================================================

@router.get("/audit-logs")
async def get_audit_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    action: str | None = Query(None),
    severity: str | None = Query(None),
    status: str | None = Query(None),
    username: str | None = Query(None),
    ip_address: str | None = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    query = db.query(AuditLog)

    if action:
        query = query.filter(
            AuditLog.action == action.upper()
        )

    if severity:
        query = query.filter(
            AuditLog.severity == severity.upper()
        )

    if status:
        query = query.filter(
            AuditLog.status == status.upper()
        )

    if username:
        query = query.filter(
            AuditLog.username == username
        )

    if ip_address:
        query = query.filter(
            AuditLog.ip_address == ip_address
        )

    total = query.count()

    offset = (page - 1) * limit

    logs = (
        query
        .order_by(AuditLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total_logs": total,
        "total_pages": (
            (total + limit - 1) // limit
            if total
            else 0
        ),

        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "action": log.action,
                "target": log.target,
                "status": log.status,
                "severity": log.severity,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "details": log.details,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }


# ============================================================
# SECURITY EVENTS
# ============================================================

@router.get("/security-events")
async def get_security_events(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    events = (
        db.query(AuditLog)
        .filter(
            AuditLog.severity.in_(
                ["WARNING", "HIGH", "CRITICAL"]
            )
        )
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "total_events": len(events),

        "events": [
            {
                "id": event.id,
                "user_id": event.user_id,
                "username": event.username,
                "action": event.action,
                "target": event.target,
                "status": event.status,
                "severity": event.severity,
                "ip_address": event.ip_address,
                "created_at": event.created_at,
            }
            for event in events
        ],
    }


# ============================================================
# SECURITY SUMMARY
# ============================================================

@router.get("/security-summary")
async def security_summary(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    since = datetime.utcnow() - timedelta(hours=24)

    recent_query = (
        db.query(AuditLog)
        .filter(AuditLog.created_at >= since)
    )

    failed_logins = (
        recent_query
        .filter(AuditLog.action == "LOGIN_FAILED")
        .count()
    )

    access_denied = (
        recent_query
        .filter(AuditLog.action == "ACCESS_DENIED")
        .count()
    )

    high_events = (
        recent_query
        .filter(AuditLog.severity == "HIGH")
        .count()
    )

    warning_events = (
        recent_query
        .filter(AuditLog.severity == "WARNING")
        .count()
    )

    top_ips = (
        recent_query
        .filter(AuditLog.ip_address.isnot(None))
        .with_entities(
            AuditLog.ip_address,
            func.count(AuditLog.id).label("event_count"),
        )
        .group_by(AuditLog.ip_address)
        .order_by(func.count(AuditLog.id).desc())
        .limit(10)
        .all()
    )

    return {
        "period": "last_24_hours",

        "events": {
            "failed_logins": failed_logins,
            "access_denied": access_denied,
            "high_severity": high_events,
            "warning": warning_events,
        },

        "top_ips": [
            {
                "ip_address": ip,
                "event_count": count,
            }
            for ip, count in top_ips
        ],
    }
