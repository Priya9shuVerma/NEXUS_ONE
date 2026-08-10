from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

from app.core.dependencies import (
    get_current_user,
    get_current_admin
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ---------------- HOME ---------------- #

@router.get("/")
async def users_home():
    return {
        "message": "Users API Working"
    }


# ---------------- GET ALL USERS (ADMIN ONLY) ---------------- #

@router.get("/all", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    users = db.query(User).all()

    return users


# ---------------- GET USER BY ID ---------------- #

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.role != "admin" and current_user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return user


# ---------------- UPDATE USER ---------------- #

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.role != "admin" and current_user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.phone is not None:
        user.phone = user_data.phone

    if user_data.bio is not None:
        user.bio = user_data.bio

    if user_data.profile_image is not None:
        user.profile_image = user_data.profile_image

    db.commit()
    db.refresh(user)

    return user


# ---------------- DELETE USER ---------------- #

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.role != "admin" and current_user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Soft Delete
    user.is_active = False

    db.commit()

    return {
        "message": "User deleted successfully"
    }