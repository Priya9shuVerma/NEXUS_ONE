from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



# ---------------- ADMIN HOME ---------------- #

@router.get("/")
async def admin_home(
    current_admin: User = Depends(get_current_admin)
):

    return {
        "message": f"Welcome Admin {current_admin.username}"
    }




# ---------------- ADMIN STATS ---------------- #

@router.get("/stats")
async def admin_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    return {

        "total_users":
            db.query(User).count(),

        "active_users":
            db.query(User)
            .filter(User.is_active == True)
            .count(),

        "admins":
            db.query(User)
            .filter(User.role=="admin")
            .count()
    }




# ---------------- DASHBOARD ---------------- #

@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )


    latest=[]


    for user in users:

        latest.append({

            "id":user.id,
            "username":user.username,
            "email":user.email,
            "role":user.role,
            "created_at":user.created_at
        })


    return {

        "system":"NEXUS ONE",

        "statistics":{

            "total_users":
            db.query(User).count(),


            "active_users":
            db.query(User)
            .filter(User.is_active==True)
            .count(),


            "inactive_users":
            db.query(User)
            .filter(User.is_active==False)
            .count(),


            "admin_users":
            db.query(User)
            .filter(User.role=="admin")
            .count()
        },


        "latest_users":latest
    }





# ---------------- GET ALL USERS ---------------- #

@router.get("/users")
async def get_all_users(

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    users=db.query(User).all()


    return {

        "total_users":len(users),

        "users":[

            {
                "id":u.id,
                "username":u.username,
                "email":u.email,
                "role":u.role,
                "is_active":u.is_active
            }

            for u in users
        ]
    }






# ---------------- DISABLE USER ---------------- #

@router.put("/disable-user/{user_id}")
async def disable_user(

    user_id:int,

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    user=db.query(User).filter(
        User.id==user_id
    ).first()


    if user is None:

        return {
            "message":"User not found"
        }


    user.is_active=False

    db.commit()


    return {

        "message":
        f"{user.username} disabled"

    }






# ---------------- ENABLE USER ---------------- #

@router.put("/enable-user/{user_id}")
async def enable_user(

    user_id:int,

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    user=db.query(User).filter(
        User.id==user_id
    ).first()


    if user is None:

        return {
            "message":"User not found"
        }


    user.is_active=True

    db.commit()


    return {

        "message":
        f"{user.username} enabled"

    }






# ---------------- MAKE ADMIN ---------------- #

@router.put("/make-admin/{user_id}")
async def make_admin(

    user_id:int,

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    user=db.query(User).filter(
        User.id==user_id
    ).first()


    if user is None:

        return {
            "message":"User not found"
        }


    user.role="admin"


    db.commit()
    db.refresh(user)


    return {

        "message":
        f"{user.username} promoted to Admin",

        "role":
        user.role
    }







# ---------------- MAKE USER ---------------- #

@router.put("/make-user/{user_id}")
async def make_user(

    user_id:int,

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    user=db.query(User).filter(
        User.id==user_id
    ).first()


    if user is None:

        return {
            "message":"User not found"
        }


    user.role="user"


    db.commit()
    db.refresh(user)


    return {

        "message":
        f"{user.username} changed to User",

        "role":
        user.role

    }







# ---------------- DELETE USER ---------------- #

@router.delete("/delete-user/{user_id}")
async def delete_user(

    user_id:int,

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):

    user=db.query(User).filter(
        User.id==user_id
    ).first()



    if user is None:

        return {
            "message":"User not found"
        }




    if user.id == current_admin.id:

        return {

            "message":
            "You cannot delete your own account"

        }



    db.delete(user)

    db.commit()



    return {

        "message":
        "User deleted successfully"

    }







# ---------------- AUDIT LOGS ---------------- #

@router.get("/audit-logs")
async def get_audit_logs(

    db:Session=Depends(get_db),

    current_admin:User=Depends(get_current_admin)

):


    logs = (

        db.query(AuditLog)

        .order_by(
            AuditLog.created_at.desc()
        )

        .all()

    )


    return {


        "total_logs":
        len(logs),


        "logs":[

            {

            "id":log.id,

            "username":log.username,

            "action":log.action,

            "target":log.target,

            "ip_address":log.ip_address,

            "created_at":log.created_at

            }

            for log in logs

        ]

    }