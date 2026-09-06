from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.iam import IAMRole, user_roles
from app.models.user import User


def get_user_roles(user_id: int, db: Session):
    return (
        db.query(IAMRole)
        .join(user_roles, IAMRole.id == user_roles.c.role_id)
        .filter(
            user_roles.c.user_id == user_id,
            IAMRole.is_active.is_(True),
        )
        .all()
    )


def get_user_permissions(user: User, db: Session):
    roles = get_user_roles(user.id, db)

    permissions = set()

    for role in roles:
        for permission in role.permissions:
            permissions.add(permission.name)

    # Backward compatibility with existing admin system.
    if user.role == "admin":
        permissions.add("*")

    return permissions


def check_permission(
    user: User,
    permission: str,
    db: Session,
    resource_owner_id: int | None = None,
    resource: str | None = None,
    action: str | None = None,
):
    """
    RBAC + ABAC authorization.

    Rules:
    1. Inactive users are denied.
    2. Explicit deny is checked first.
    3. Existing admin users retain full access.
    4. Exact permission grants access.
    5. Resource ownership can grant access.
    """

    if not user.is_active:
        return False

    permissions = get_user_permissions(user, db)

    # Explicit deny always wins.
    if f"deny:{permission}" in permissions:
        return False

    if resource and action:
        if f"deny:{resource}:{action}" in permissions:
            return False

    # Existing admin compatibility.
    if "*" in permissions:
        return True

    # Exact RBAC permission.
    if permission in permissions:
        return True

    # ABAC: resource ownership.
    if (
        resource_owner_id is not None
        and resource_owner_id == user.id
        and resource
        and action
        and f"{resource}:own:{action}" in permissions
    ):
        return True

    return False


def require_permission(permission: str):
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        allowed = check_permission(
            current_user,
            permission,
            db,
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "ACCESS_DENIED",
                    "required_permission": permission,
                },
            )

        return current_user

    return dependency
