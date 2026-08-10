import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta, datetime

from app.core.security import sha256_hex
import uuid
from app.core.jwt import create_refresh_token, create_access_token
from app.models.token import RefreshToken
from app.models.blacklist_token import BlacklistToken


# A. SHA-256 helper tests (length/determinism)
def test_sha256_properties():
    a = sha256_hex("sampletoken")
    b = sha256_hex("sampletoken")
    c = sha256_hex("sampletoken2")

    assert a == b
    assert a != c
    # hex length for SHA-256 is 64
    assert isinstance(a, str) and len(a) == 64


# B. Login token storage
def test_login_stores_hashed_refresh(client, db_session, create_test_user):
    user, password = create_test_user()

    resp = client.post("/auth/login", json={"email": user.email, "password": password})
    assert resp.status_code == 200
    j = resp.json()
    assert "access_token" in j and "refresh_token" in j

    # find the latest refresh token row for this user
    row = db_session.query(RefreshToken).filter(RefreshToken.user_id == user.id).order_by(RefreshToken.id.desc()).first()
    assert row is not None
    # token_hash must be present and token must NOT contain raw value (we store placeholder for new rows)
    assert row.token_hash is not None and row.token_hash != ''
    assert (row.token is None) or (row.token == '') or (isinstance(row.token, str) and row.token.startswith('removed_'))

    # token_hash should equal sha256_hex(refresh_token) — compute in memory and compare (do not print)
    assert row.token_hash == sha256_hex(j["refresh_token"])


# C/D. Refresh rotation and replay protection
def test_refresh_rotation_and_replay(client, db_session, create_test_user):
    user, password = create_test_user()

    login = client.post("/auth/login", json={"email": user.email, "password": password})
    assert login.status_code == 200
    data = login.json()
    refresh = data["refresh_token"]

    # Call refresh once
    r1 = client.post("/auth/refresh-token", json={"refresh_token": refresh})
    assert r1.status_code == 200
    d1 = r1.json()
    assert "refresh_token" in d1 and "access_token" in d1

    # After rotation, old token must be inactive — retrying should fail
    r2 = client.post("/auth/refresh-token", json={"refresh_token": refresh})
    assert r2.status_code == 401

    # Verify new refresh row stored hash only
    new_refresh = d1["refresh_token"]
    row = db_session.query(RefreshToken).filter(RefreshToken.user_id == user.id).order_by(RefreshToken.id.desc()).first()
    assert row is not None
    assert row.token_hash == sha256_hex(new_refresh)
    assert (row.token is None) or (row.token == '') or (isinstance(row.token, str) and row.token.startswith('removed_'))


# E. Concurrent refresh test
def test_concurrent_refresh_attempts(client, db_session, create_test_user):
    user, password = create_test_user()

    login = client.post("/auth/login", json={"email": user.email, "password": password})
    assert login.status_code == 200
    data = login.json()
    refresh = data["refresh_token"]

    # capture active refresh count before
    before_active = db_session.query(RefreshToken).filter(RefreshToken.user_id == user.id, RefreshToken.is_active == True).count()

    # send two concurrent refresh requests
    def do_refresh():
        # use a fresh TestClient in each thread to reduce shared state issues
        from fastapi.testclient import TestClient
        from app.main import app
        with TestClient(app) as c:
            resp = c.post("/auth/refresh-token", json={"refresh_token": refresh})
            return resp.status_code, resp.json() if resp.status_code == 200 else None

    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(do_refresh) for _ in range(2)]
        for fut in as_completed(futures):
            results.append(fut.result())

    successes = [r for r in results if r[0] == 200]
    failures = [r for r in results if r[0] != 200]

    # Exactly one should succeed, one should fail
    assert len(successes) == 1
    assert len(failures) == 1

    # after requests, active refresh count should have increased by at most 1
    after_active = db_session.query(RefreshToken).filter(RefreshToken.user_id == user.id, RefreshToken.is_active == True).count()
    assert after_active - before_active <= 1


# F. Blacklist test (logout revokes refresh and blacklists access)
def test_logout_blacklist_behavior(client, db_session, create_test_user):
    user, password = create_test_user()

    login = client.post("/auth/login", json={"email": user.email, "password": password})
    assert login.status_code == 200
    data = login.json()
    access = data["access_token"]
    refresh = data["refresh_token"]

    # auth-protected endpoint should succeed
    headers = {"Authorization": f"Bearer {access}"}
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200

    # logout
    logout = client.post("/auth/logout", json={"refresh_token": refresh}, headers=headers)
    assert logout.status_code == 200

    # subsequent request with same access token should be rejected
    me2 = client.get("/auth/me", headers=headers)
    assert me2.status_code == 401

    # verify blacklist DB row exists and stores token_hash (not raw token)
    bl = db_session.query(BlacklistToken).order_by(BlacklistToken.id.desc()).first()
    assert bl is not None
    assert bl.token_hash is not None and bl.token_hash != ''
    assert (bl.token is None) or (bl.token == '') or (isinstance(bl.token, str) and bl.token.startswith('removed_'))


# G. Legacy plaintext compatibility
def test_legacy_plaintext_refresh_migration(client, db_session, create_test_user):
    user, password = create_test_user()

    # create a valid refresh token JWT
    raw_refresh = create_refresh_token({"user_id": user.id, "email": user.email, "role": user.role})

    # insert a legacy row: token plaintext set, token_hash NULL
    legacy = RefreshToken(user_id=user.id, token=raw_refresh, token_hash=None, is_active=True, expires_at=datetime.utcnow() + timedelta(days=7))
    db_session.add(legacy)
    db_session.commit()
    db_session.refresh(legacy)

    # use it
    resp = client.post("/auth/refresh-token", json={"refresh_token": raw_refresh})
    assert resp.status_code == 200

    # refresh the test session's view of the legacy row, then assert migration
    db_session.refresh(legacy)
    migrated = db_session.query(RefreshToken).filter(RefreshToken.id == legacy.id).first()
    assert migrated is not None
    assert migrated.token_hash is not None and migrated.token_hash != ''
    assert (migrated.token is None) or (migrated.token == '') or (isinstance(migrated.token, str) and migrated.token.startswith('removed_'))


# H. Invalid token tests
def test_invalid_and_expired_tokens(client, db_session, create_test_user):
    user, password = create_test_user()

    # invalid access token for protected endpoint
    bad_headers = {"Authorization": "Bearer notavalid.token.here"}
    r = client.get("/auth/me", headers=bad_headers)
    assert r.status_code == 401

    # invalid refresh token
    r2 = client.post("/auth/refresh-token", json={"refresh_token": "notavalidtoken"})
    assert r2.status_code == 401

    # expired refresh token (create with negative expiry)
    expired = create_refresh_token({"user_id": user.id}, expires_delta=timedelta(seconds=-10))
    # store in DB hashed
    row = RefreshToken(user_id=user.id, token=f"removed_{uuid.uuid4().hex}", token_hash=sha256_hex(expired), is_active=True, expires_at=datetime.utcnow() - timedelta(days=1))
    db_session.add(row)
    db_session.commit()

    r3 = client.post("/auth/refresh-token", json={"refresh_token": expired})
    assert r3.status_code == 401

    # inactive refresh token
    inactive = create_refresh_token({"user_id": user.id})
    row2 = RefreshToken(user_id=user.id, token=f"removed_{uuid.uuid4().hex}", token_hash=sha256_hex(inactive), is_active=False, expires_at=datetime.utcnow() + timedelta(days=7))
    db_session.add(row2)
    db_session.commit()

    r4 = client.post("/auth/refresh-token", json={"refresh_token": inactive})
    assert r4.status_code == 401


# I. Security regression checks (sanity)
def test_security_regressions_dont_store_raw_tokens(client, db_session, create_test_user):
    user, password = create_test_user()
    resp = client.post("/auth/login", json={"email": user.email, "password": password})
    assert resp.status_code == 200
    j = resp.json()
    refresh = j["refresh_token"]

    # latest refresh row should not store raw token
    row = db_session.query(RefreshToken).filter(RefreshToken.user_id == user.id).order_by(RefreshToken.id.desc()).first()
    assert row is not None
    assert (row.token is None) or (row.token == '') or (isinstance(row.token, str) and row.token.startswith('removed_'))
    assert row.token_hash == sha256_hex(refresh)

    # blacklist behavior: logout then check row
    headers = {"Authorization": f"Bearer {j['access_token']}"}
    logout = client.post("/auth/logout", json={"refresh_token": refresh}, headers=headers)
    assert logout.status_code == 200
    bl = db_session.query(BlacklistToken).order_by(BlacklistToken.id.desc()).first()
    assert bl is not None
    assert (bl.token is None) or (bl.token == '') or (isinstance(bl.token, str) and bl.token.startswith('removed_'))
    assert bl.token_hash is not None and len(bl.token_hash) == 64
