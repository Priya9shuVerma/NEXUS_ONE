from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.iam import (
    IAMPermission,
    IAMRole,
    role_permissions,
    user_roles,
)
from app.models.user import User


router = APIRouter(
    prefix="/iam",
    tags=["IAM"],
)


# =========================
# ROLES
# =========================

@router.get("/roles")
def get_roles(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    roles = db.query(IAMRole).all()

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "is_active": role.is_active,
            "permissions": [p.name for p in role.permissions],
        }
        for role in roles
    ]


@router.post("/roles")
def create_role(
    name: str,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    existing = db.query(IAMRole).filter(IAMRole.name == name).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Role already exists",
        )

    role = IAMRole(
        name=name,
        description=description,
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return {
        "message": "Role created",
        "id": role.id,
        "name": role.name,
    }


# =========================
# PERMISSIONS
# =========================

@router.get("/permissions")
def get_permissions(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    permissions = db.query(IAMPermission).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "resource": p.resource,
            "action": p.action,
            "description": p.description,
        }
        for p in permissions
    ]


@router.post("/permissions")
def create_permission(
    name: str,
    resource: str,
    action: str,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    existing = (
        db.query(IAMPermission)
        .filter(IAMPermission.name == name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Permission already exists",
        )

    permission = IAMPermission(
        name=name,
        resource=resource,
        action=action,
        description=description,
    )

    db.add(permission)
    db.commit()
    db.refresh(permission)

    return {
        "message": "Permission created",
        "id": permission.id,
        "name": permission.name,
    }


# =========================
# ROLE → PERMISSION
# =========================

@router.post("/roles/{role_id}/permissions/{permission_id}")
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    role = db.query(IAMRole).filter(IAMRole.id == role_id).first()
    permission = (
        db.query(IAMPermission)
        .filter(IAMPermission.id == permission_id)
        .first()
    )

    if not role:
        raise HTTPException(404, "Role not found")

    if not permission:
        raise HTTPException(404, "Permission not found")

    if permission in role.permissions:
        return {
            "message": "Permission already assigned",
            "role": role.name,
            "permission": permission.name,
        }

    role.permissions.append(permission)

    db.commit()

    return {
        "message": "Permission assigned to role",
        "role": role.name,
        "permission": permission.name,
    }


@router.delete("/roles/{role_id}/permissions/{permission_id}")
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    role = db.query(IAMRole).filter(IAMRole.id == role_id).first()
    permission = (
        db.query(IAMPermission)
        .filter(IAMPermission.id == permission_id)
        .first()
    )

    if not role:
        raise HTTPException(404, "Role not found")

    if not permission:
        raise HTTPException(404, "Permission not found")

    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()

    return {
        "message": "Permission removed from role",
        "role": role.name,
        "permission": permission.name,
    }


# =========================
# USER → ROLE
# =========================

@router.post("/users/{user_id}/roles/{role_id}")
def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(IAMRole).filter(IAMRole.id == role_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if not role:
        raise HTTPException(404, "Role not found")

    exists = db.execute(
        user_roles.select().where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role_id,
        )
    ).first()

    if exists:
        return {
            "message": "Role already assigned",
            "user_id": user_id,
            "role": role.name,
        }

    db.execute(
        user_roles.insert().values(
            user_id=user_id,
            role_id=role_id,
        )
    )

    db.commit()

    return {
        "message": "Role assigned to user",
        "user_id": user_id,
        "role": role.name,
    }


@router.delete("/users/{user_id}/roles/{role_id}")
def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(IAMRole).filter(IAMRole.id == role_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if not role:
        raise HTTPException(404, "Role not found")

    db.execute(
        user_roles.delete().where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role_id,
        )
    )

    db.commit()

    return {
        "message": "Role removed from user",
        "user_id": user_id,
        "role": role.name,
    }


# =========================
# CURRENT USER IAM
# =========================

@router.get("/me")
def get_my_iam(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    roles = (
        db.query(IAMRole)
        .join(
            user_roles,
            IAMRole.id == user_roles.c.role_id,
        )
        .filter(
            user_roles.c.user_id == current_user.id,
            IAMRole.is_active.is_(True),
        )
        .all()
    )

    permissions = []

    for role in roles:
        for permission in role.permissions:
            if permission.name not in permissions:
                permissions.append(permission.name)

    # Existing admin role gets full administrative compatibility.
    if current_user.role == "admin":
        permissions.append("*")

    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "legacy_role": current_user.role,
        "roles": [role.name for role in roles],
        "permissions": sorted(set(permissions)),
    }
