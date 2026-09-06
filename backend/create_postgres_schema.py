from sqlalchemy import create_engine

from app.db.database import Base

from app.models.user import User
from app.models.token import RefreshToken
from app.models.chat_history import ChatHistory
from app.models.audit_log import AuditLog
from app.models.blacklist_token import BlacklistToken
from app.models.password_reset_token import PasswordResetToken
from app.models.security_event import SecurityEvent

POSTGRES_URL = "postgresql+psycopg://nexus_admin:nexus_local_password@127.0.0.1:5432/nexus_one"

engine = create_engine(POSTGRES_URL)

print("Creating PostgreSQL schema...")

Base.metadata.create_all(bind=engine)

print("POSTGRESQL SCHEMA: CREATED")
