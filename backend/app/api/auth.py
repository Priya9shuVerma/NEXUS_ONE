from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.security.rate_limit.limiter import rate_limit


from app.db.database import get_db


from app.models.user import User
from app.models.token import RefreshToken
from app.models.blacklist_token import BlacklistToken
from app.models.password_reset_token import PasswordResetToken


from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordChange,
    ForgotPasswordRequest,
    ResetPasswordRequest
)


from app.core.security import (
    hash_password,
    verify_password,
    sha256_hex
)


from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)

import logging
logger = logging.getLogger(__name__)


from app.core.dependencies import get_current_user


from app.services.audit_service import save_audit_log
from app.services.login_security import (
    record_failed_login,
    is_suspicious_login,
    record_suspicious_login,
)

from app.services.account_security import (
    is_account_locked,
    register_failed_attempt,
    register_successful_login,
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
security = HTTPBearer()



# ---------------- HOME ---------------- #

@router.get("/")
async def auth_home():

    return {
        "message": "Authentication API Working"
    }





# ---------------- REGISTER ---------------- #

@router.post(
    "/register",
    dependencies=[
        Depends(
            rate_limit(
                max_requests=3,
                window=60
            )
        )
    ]
)
async def register(

    request: Request,

    user: UserCreate,

    db: Session = Depends(get_db)

):


    existing_username = db.query(User).filter(
        User.username == user.username
    ).first()



    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )



    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()



    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )




    new_user = User(

        username=user.username,

        email=user.email,

        hashed_password=hash_password(
            user.password
        ),

        role="user"

    )



    db.add(new_user)

    db.commit()

    db.refresh(new_user)




    save_audit_log(

        db=db,

        user_id=new_user.id,

        username=new_user.username,

        action="REGISTER",

        target="AUTH",

        ip_address=request.client.host

    )



    return {


        "message": "User Registered Successfully",


        "id": new_user.id,


        "username": new_user.username,


        "email": new_user.email,


        "role": new_user.role

    }





# ---------------- LOGIN ---------------- #


@router.post(
    "/login",
    dependencies=[
        Depends(
            rate_limit(
                max_requests=5,
                window=60
            )
        )
    ]
)
async def login(

    request: Request,

    user: UserLogin,

    db: Session = Depends(get_db)

):


    db_user = db.query(User).filter(

        User.email == user.email

    ).first()




    # INVALID EMAIL

    if not db_user:


        save_audit_log(

            db=db,

            user_id=None,

            username=user.email,

            action="LOGIN_FAILED",

            target="Invalid Email",

            ip_address=request.client.host

        )


        raise HTTPException(

            status_code=401,

            detail="Invalid Email or Password"

        )





    # WRONG PASSWORD


    if not verify_password(

        user.password,

        db_user.hashed_password

    ):


        save_audit_log(

            db=db,

            user_id=db_user.id,

            username=db_user.username,

            action="LOGIN_FAILED",

            target="Wrong Password",

            ip_address=request.client.host

        )



        raise HTTPException(

            status_code=401,

            detail="Invalid Email or Password"

        )





    # ACCESS TOKEN


    access_token = create_access_token(

        {

            "user_id": db_user.id,

            "email": db_user.email,

            "role": db_user.role

        }

    )




    # REFRESH TOKEN


    refresh_token = create_refresh_token(

        {

            "user_id": db_user.id,

            "email": db_user.email,

            "role": db_user.role

        }

    )




    new_refresh_token = RefreshToken(

        user_id=db_user.id,

        token=f"removed_{uuid.uuid4().hex}",

        token_hash=sha256_hex(refresh_token)

    )



    db.add(new_refresh_token)

    db.commit()




    save_audit_log(

        db=db,

        user_id=db_user.id,

        username=db_user.username,

        action="LOGIN_SUCCESS",

        target="AUTH",

        ip_address=request.client.host

    )



    return {


        "message": "Login Successful",


        "access_token": access_token,


        "refresh_token": refresh_token,


        "token_type": "bearer",


        "username": db_user.username,


        "email": db_user.email,


        "role": db_user.role

    }

# ---------------- REFRESH TOKEN ---------------- #

@router.post("/refresh-token")
async def refresh_token(

    refresh_token: str = Body(..., embed=True),

    db: Session = Depends(get_db)

):

    payload = verify_refresh_token(refresh_token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh Token"
        )

    user_id = payload.get("user_id")
    email = payload.get("email")
    role = payload.get("role")

    # Compute incoming hash and try hashed lookup first
    incoming_hash = sha256_hex(refresh_token)

    stored_token = db.query(
        RefreshToken
    ).filter(
        RefreshToken.token_hash == incoming_hash,
        RefreshToken.is_active == True
    ).first()

    # Legacy plaintext fallback
    if not stored_token:
        stored_token = db.query(
            RefreshToken
        ).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_active == True
        ).first()

    if not stored_token:

        raise HTTPException(
            status_code=401,
            detail="Refresh Token Expired"
        )

    # Check Expiry
    if stored_token.expires_at < datetime.utcnow():

        stored_token.is_active = False
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh Token Expired"
        )

    # ---------------- ROTATE TOKEN (atomic) ---------------- #

    # Attempt atomic consumption of the stored token by updating is_active -> False
    # only if it is still active. Use incoming hash if available.
    incoming_hash = sha256_hex(refresh_token)

    # Prefer hashed match
    update_stmt = None
    if stored_token.token_hash:
        update_stmt = (
            RefreshToken.__table__.update()
            .where(
                (RefreshToken.id == stored_token.id) &
                (RefreshToken.is_active == True) &
                (RefreshToken.token_hash == incoming_hash)
            )
            .values(is_active=False)
        )
    else:
        # Legacy plaintext row — match by token value
        update_stmt = (
            RefreshToken.__table__.update()
            .where(
                (RefreshToken.id == stored_token.id) &
                (RefreshToken.is_active == True) &
                (RefreshToken.token == refresh_token)
            )
            .values(is_active=False)
        )

    result = db.execute(update_stmt)
    logger.info(f"refresh consume update rowcount={getattr(result, 'rowcount', 'unknown')} for id={stored_token.id}")
    if result.rowcount == 0:
        # Token already consumed by another request
        raise HTTPException(status_code=401, detail="Refresh Token Expired")

    # If this was a legacy plaintext row, migrate it to hashed storage (remove plaintext)
    try:
        if not stored_token.token_hash:
            placeholder = f"removed_{uuid.uuid4().hex}"
            db.execute(
                RefreshToken.__table__.update()
                .where(RefreshToken.id == stored_token.id)
            .values(token_hash=incoming_hash, token=placeholder)
            )
            logger.info(f"migrated legacy refresh id={stored_token.id} to hashed storage")
    except Exception:
        # Migration best-effort: do not fail refresh if migration write fails
        logger.exception("Failed migrating legacy refresh token to hashed storage")
        db.rollback()

    db.commit()

    # Create and store new refresh token (store hash only)
    new_refresh_token = create_refresh_token(

        {
            "user_id": user_id,
            "email": email,
            "role": role
        }

    )

    db.add(

        RefreshToken(

            user_id=user_id,
        token=f"removed_{uuid.uuid4().hex}",
            token_hash=sha256_hex(new_refresh_token),
            expires_at=datetime.utcnow() + timedelta(days=7)

        )

    )

    db.commit()

    new_access_token = create_access_token(

        {
            "user_id": user_id,
            "email": email,
            "role": role
        }

    )

    return {

        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"

    }


# ---------------- LOGOUT ---------------- #

@router.post("/logout")
async def logout(

    request: Request,

    refresh_token: str = Body(..., embed=True),

    credentials: HTTPAuthorizationCredentials = Depends(security),

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    # ---------------- DISABLE REFRESH TOKEN ---------------- #

    incoming_hash = None
    try:
        incoming_hash = sha256_hex(refresh_token)
    except Exception:
        incoming_hash = None

    token = None
    if incoming_hash:
        token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == incoming_hash
        ).first()

    if not token:
        token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ).first()

    if token:
        token.is_active = False
        # For legacy rows, migrate token to hashed storage (best-effort)
        try:
            if not token.token_hash:
                token.token_hash = incoming_hash
                placeholder = f"removed_{uuid.uuid4().hex}"
                token.token = placeholder
                db.add(token)
        except Exception:
            db.rollback()

    # ---------------- BLACKLIST ACCESS TOKEN ---------------- #

    access_token = credentials.credentials

    access_hash = sha256_hex(access_token)

    existing_blacklist = db.query(
        BlacklistToken
    ).filter(
        (BlacklistToken.token_hash == access_hash) | (BlacklistToken.token == access_token)
    ).first()

    if not existing_blacklist:

        blacklist_token = BlacklistToken(
            token=f"removed_{uuid.uuid4().hex}",
            token_hash=access_hash
        )

        db.add(blacklist_token)

    db.commit()

    # ---------------- AUDIT LOG ---------------- #

    save_audit_log(

        db=db,

        user_id=current_user.id,

        username=current_user.username,

        action="LOGOUT",

        target="AUTH",

        ip_address=request.client.host

    )

    return {

        "message": "Logout Successful"

    }


# ---------------- CURRENT USER ---------------- #

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(

    current_user: User = Depends(
        get_current_user
    )

):

    return current_user




# ---------------- UPDATE PROFILE ---------------- #

@router.put("/profile")

async def update_profile(

    request: Request,

    data: UserUpdate,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):


    if data.full_name is not None:

        current_user.full_name = data.full_name



    if data.phone is not None:

        current_user.phone = data.phone



    if data.bio is not None:

        current_user.bio = data.bio



    if data.profile_image is not None:

        current_user.profile_image = data.profile_image


    db.commit()

    db.refresh(current_user)

    save_audit_log(

        db=db,

        user_id=current_user.id,

        username=current_user.username,

        action="PROFILE_UPDATE",

        target="USER",

        ip_address=request.client.host

    )

    return {


        "message": "Profile Updated Successfully",


        "id": current_user.id

    }



# ---------------- FORGOT PASSWORD ----------------

@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # Do not reveal whether an email exists.
    if not user:
        return {
            "message": "If the account exists, a password reset request has been created."
        }

    # Invalidate existing unused reset tokens for this user.
    existing_tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None)
    ).all()

    for reset_token in existing_tokens:
        reset_token.used_at = datetime.utcnow()

    # Generate a random reset token.
    raw_token = uuid.uuid4().hex + uuid.uuid4().hex

    # Store only the SHA-256 hash.
    token_hash = sha256_hex(raw_token)

    reset_record = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.add(reset_record)
    db.commit()

    return {
        "message": "Password reset request created.",
        "reset_token": raw_token
    }


# ---------------- RESET PASSWORD ----------------

@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    token_hash = sha256_hex(data.token)

    reset_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash
    ).first()

    if not reset_record:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    if reset_record.used_at is not None:
        raise HTTPException(
            status_code=400,
            detail="Reset token has already been used"
        )

    if reset_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    user = db.query(User).filter(
        User.id == reset_record.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset request"
        )

    user.hashed_password = hash_password(
        data.new_password
    )

    reset_record.used_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Password reset successfully"
    }


# ---------------- CHANGE PASSWORD ---------------- #


@router.put("/change-password")

async def change_password(

    request: Request,

    data: PasswordChange,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):



    if not verify_password(

        data.old_password,

        current_user.hashed_password

    ):


        raise HTTPException(

            status_code=400,

            detail="Old password is incorrect"

        )





    current_user.hashed_password = hash_password(

        data.new_password

    )



    db.commit()

    db.refresh(current_user)





    save_audit_log(

        db=db,

        user_id=current_user.id,

        username=current_user.username,

        action="PASSWORD_CHANGED",

        target="AUTH",

        ip_address=request.client.host

    )





    return {


        "message": "Password Changed Successfully"

    }








