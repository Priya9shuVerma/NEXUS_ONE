import os
import sys
import uuid
from typing import Generator

# Ensure backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure minimal env for app import
os.environ.setdefault('DATABASE_URL', 'sqlite:///C:/NEXUS_ONE/backend/nexus_one.db')
os.environ.setdefault('SECRET_KEY', 'placeholder_secret_for_tests')

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


@pytest.fixture(scope='session')
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def create_test_user(db_session):
    created = []

    def _create(email=None):
        username = f"test_user_{uuid.uuid4().hex[:8]}"
        email = email or f"{username}@example.com"
        password = "TestPass123!"
        user = User(username=username, email=email, hashed_password=hash_password(password), role='user')
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        created.append(user)
        return user, password

    yield _create

    # cleanup: delete created users and their tokens if possible
    for u in created:
        try:
            db_session.delete(u)
            db_session.commit()
        except Exception:
            db_session.rollback()
