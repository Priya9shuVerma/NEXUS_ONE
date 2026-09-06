from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from fastapi.middleware.cors import CORSMiddleware

from app.middleware.logging import RequestLoggingMiddleware

from app.security.headers import SecurityHeadersMiddleware
from app.security.middleware.security import SecurityMiddleware

from app.models.chat_history import ChatHistory

from app.exceptions.handler import (
    global_exception_handler,
    database_exception_handler
)


from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router
from app.api.cloud import router as cloud_router
from app.api.jit import router as jit_router
from app.api.iam import router as iam_router


from app.db.database import Base, engine


# Import models for table creation
from app.models import token
from app.models import user
from app.models import audit_log
from app.models import blacklist_token
from app.models import password_reset_token
from app.models.cloud import CloudAccount, CloudAsset



# Create Database Tables
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="NEXUS ONE API",
    version="0.1.0",
    description="AI + Cybersecurity + Full Stack Platform"
)



# ---------------- EXCEPTION HANDLERS ---------------- #

app.add_exception_handler(
    Exception,
    global_exception_handler
)


app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)



# ---------------- MIDDLEWARE ---------------- #

# Request Logging Middleware

app.add_middleware(
    RequestLoggingMiddleware
)


# Security Monitoring Middleware

app.add_middleware(
    SecurityMiddleware
)

# Security Headers Middleware

app.add_middleware(
    SecurityHeadersMiddleware
)


# CORS Middleware

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)



# ---------------- ROUTES ---------------- #

# Authentication

app.include_router(
    auth_router
)


# Users

app.include_router(
    users_router
)


# Admin

app.include_router(
    admin_router
)



# ---------------- DEFAULT ROUTES ---------------- #

@app.get("/")
def root():

    return {
        "message": "NEXUS ONE API Running"
    }



@app.get("/health")
def health():

    return {
        "status": "OK"
    }
from app.api.ai import router as ai_router

app.include_router(ai_router)

from app.models import security_event
from app.api.security import router as security_router

app.include_router(security_router)




# ---------------- CLOUD SECURITY ----------------
app.include_router(cloud_router)



app.include_router(iam_router)

app.include_router(jit_router)



from app.models import jea

from app.api.jea import router as jea_router

app.include_router(jea_router)

from app.api.audit import router as audit_router

app.include_router(audit_router)
