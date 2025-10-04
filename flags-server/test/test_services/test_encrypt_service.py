from src.services.encrypt_service import EncryptService


def test_password_property() -> None:
    enc = EncryptService("secret123")
    assert enc.password == "secret123"


def test_password_hashed_is_different() -> None:
    enc = EncryptService("secret123")
    hashed = enc.password_hashed

    assert isinstance(hashed, str)
    assert hashed != enc.password
    assert hashed.startswith(("pbkdf2:", "scrypt:"))


def test_valid_password_correct() -> None:
    password = "secret123"
    enc = EncryptService(password)
    hashed = enc.password_hashed

    assert enc.valid_password(hashed) is True


def test_valid_password_incorrect() -> None:
    enc = EncryptService("wrongpassword")
    other_hash = EncryptService("secret123").password_hashed

    assert enc.valid_password(other_hash) is False
