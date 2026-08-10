from app.core.security import sha256_hex


def test_sha256_same_input():
    a = sha256_hex("token123")
    b = sha256_hex("token123")
    assert a == b


def test_sha256_different_input():
    a = sha256_hex("token123")
    b = sha256_hex("token124")
    assert a != b
